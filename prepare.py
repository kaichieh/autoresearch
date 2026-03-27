"""
One-time data preparation for GLD direction experiments.

Downloads daily GLD prices, engineers a small feature set, and stores
chronological train/validation/test splits for downstream experiments.

Usage:
    python prepare.py
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
import requests

HORIZON_DAYS = 3
TRAIN_FRACTION = 0.70
VALID_FRACTION = 0.15
TEST_FRACTION = 0.15

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(REPO_DIR, ".cache", "autoresearch-gld")
RAW_DATA_PATH = os.path.join(CACHE_DIR, "gld_daily.csv")
PROCESSED_DATA_PATH = os.path.join(CACHE_DIR, "gld_features.csv")
METADATA_PATH = os.path.join(CACHE_DIR, "metadata.json")

GLD_STOOQ_URL = "https://stooq.com/q/d/l/?s=gld.us&i=d"
FEATURE_COLUMNS = [
    "ret_1",
    "ret_3",
    "ret_5",
    "ret_10",
    "ret_20",
    "sma_gap_5",
    "sma_gap_10",
    "sma_gap_20",
    "volatility_5",
    "volatility_10",
    "range_pct",
    "volume_change_1",
    "volume_vs_20",
]
TARGET_COLUMN = "target_up"


@dataclass(frozen=True)
class DatasetSplit:
    features: np.ndarray
    labels: np.ndarray
    frame: pd.DataFrame


def ensure_cache_dir() -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)


def download_gld_prices() -> pd.DataFrame:
    ensure_cache_dir()
    response = requests.get(GLD_STOOQ_URL, timeout=30)
    response.raise_for_status()
    with open(RAW_DATA_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(response.text)
    frame = pd.read_csv(RAW_DATA_PATH)
    if frame.empty:
        raise RuntimeError("Downloaded GLD dataset is empty.")
    return frame


def add_features(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.copy()
    df.columns = [column.lower() for column in df.columns]
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    close = df["close"]
    volume = df["volume"].replace(0, np.nan)

    df["ret_1"] = close.pct_change(1)
    df["ret_3"] = close.pct_change(3)
    df["ret_5"] = close.pct_change(5)
    df["ret_10"] = close.pct_change(10)
    df["ret_20"] = close.pct_change(20)

    df["sma_gap_5"] = close / close.rolling(5).mean() - 1.0
    df["sma_gap_10"] = close / close.rolling(10).mean() - 1.0
    df["sma_gap_20"] = close / close.rolling(20).mean() - 1.0

    df["volatility_5"] = df["ret_1"].rolling(5).std()
    df["volatility_10"] = df["ret_1"].rolling(10).std()
    df["range_pct"] = (df["high"] - df["low"]) / close

    df["volume_change_1"] = volume.pct_change(1)
    df["volume_vs_20"] = volume / volume.rolling(20).mean() - 1.0

    # Extra features for extended model
    df["breakout_20"] = (close > close.shift(1).rolling(20).max()).astype(float)
    df["drawdown_20"] = (close - close.rolling(20).max()) / close.rolling(20).max()
    
    # RSI-14
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / (loss + 1e-10)
    df["rsi_14"] = 100 - (100 / (1 + rs))

    future_close = close.shift(-HORIZON_DAYS)
    df[TARGET_COLUMN] = (future_close > close).astype(int)
    df["future_return"] = future_close / close - 1.0

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN, "future_return"]).reset_index(drop=True)
    return df


def split_indices(num_rows: int) -> tuple[int, int]:
    train_end = int(num_rows * TRAIN_FRACTION)
    valid_end = train_end + int(num_rows * VALID_FRACTION)
    if train_end <= 0 or valid_end >= num_rows:
        raise RuntimeError("Not enough rows to create chronological train/validation/test splits.")
    return train_end, valid_end


def save_processed_dataset(df: pd.DataFrame) -> None:
    train_end, valid_end = split_indices(len(df))
    ensure_cache_dir()
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    metadata = {
        "symbol": "GLD",
        "horizon_days": HORIZON_DAYS,
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
        "train_rows": train_end,
        "validation_rows": valid_end - train_end,
        "test_rows": len(df) - valid_end,
        "total_rows": len(df),
        "date_start": df["date"].iloc[0].strftime("%Y-%m-%d"),
        "date_end": df["date"].iloc[-1].strftime("%Y-%m-%d"),
    }
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def load_dataset_frame() -> pd.DataFrame:
    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(
            f"Processed dataset not found at {PROCESSED_DATA_PATH}. Run prepare.py first."
        )
    df = pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["date"])
    missing = [column for column in FEATURE_COLUMNS + [TARGET_COLUMN, "future_return"] if column not in df.columns]
    if missing:
        raise RuntimeError(f"Processed dataset is missing expected columns: {missing}")
    return df


def load_splits() -> dict[str, DatasetSplit]:
    df = load_dataset_frame()
    train_end, valid_end = split_indices(len(df))
    splits = {
        "train": df.iloc[:train_end].copy(),
        "validation": df.iloc[train_end:valid_end].copy(),
        "test": df.iloc[valid_end:].copy(),
    }
    output: dict[str, DatasetSplit] = {}
    for name, frame in splits.items():
        output[name] = DatasetSplit(
            features=frame[FEATURE_COLUMNS].to_numpy(dtype=np.float32),
            labels=frame[TARGET_COLUMN].to_numpy(dtype=np.float32),
            frame=frame,
        )
    return output


def describe_dataset(df: pd.DataFrame) -> str:
    train_end, valid_end = split_indices(len(df))
    up_rate = df[TARGET_COLUMN].mean()
    lines = [
        f"Rows: {len(df)}",
        f"Date range: {df['date'].iloc[0].date()} -> {df['date'].iloc[-1].date()}",
        f"Train/validation/test: {train_end}/{valid_end - train_end}/{len(df) - valid_end}",
        f"Positive class rate: {up_rate:.3f}",
        f"Features: {', '.join(FEATURE_COLUMNS)}",
        f"Cache directory: {CACHE_DIR}",
    ]
    return "\n".join(lines)


def main() -> None:
    print("Downloading GLD daily prices...")
    raw = download_gld_prices()
    processed = add_features(raw)
    save_processed_dataset(processed)
    print("Prepared dataset:")
    print(describe_dataset(processed))
    print(f"Raw data saved to: {RAW_DATA_PATH}")
    print(f"Processed data saved to: {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    main()
