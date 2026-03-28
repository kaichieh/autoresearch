"""
Train a simple GLD 3-day direction classifier.

The goal is not to predict the exact price. We only predict whether GLD
will close higher or lower three trading days from now.

Usage:
    python train.py
"""

from __future__ import annotations

import math
import os
import random
from dataclasses import dataclass

import numpy as np

from prepare import FEATURE_COLUMNS, HORIZON_DAYS, TARGET_COLUMN, load_splits

SEED = 42
LEARNING_RATE = 0.02
L2_REG = 1e-3
MAX_EPOCHS = 1200
PATIENCE = 120
POS_WEIGHT = 1.0
NEG_WEIGHT = 1.3
THRESHOLD_OBJECTIVE = "f1"
THRESHOLD_MIN = 0.30
THRESHOLD_MAX = 0.70
THRESHOLD_STEPS = 401
EXTRA_FEATURE_COLUMNS = ("breakout_20", "drawdown_20", "rsi_14")
DROP_FEATURE_COLUMNS = ("ret_1", "volume_change_1")
DERIVED_FEATURE_COLUMNS = ("overnight_gap", "intraday_return")
INTERACTION_FEATURE_PAIRS = (
    ("ret_1", "ret_3"),
    ("ret_5", "volatility_5"),
    ("ret_3", "breakout_20"),
    ("ret_20", "volatility_10"),
    ("ret_20", "sma_gap_10"),
    ("sma_gap_5", "sma_gap_20"),
    ("ret_1", "range_pct"),
    ("ret_10", "volume_change_1"),
    ("volume_change_1", "breakout_20"),
    ("range_pct", "volume_vs_20"),
    ("volume_vs_20", "drawdown_20"),
    ("intraday_return", "volume_vs_20"),
    ("overnight_gap", "volume_vs_20"),
)


@dataclass
class Metrics:
    loss: float
    accuracy: float
    precision: float
    recall: float
    f1: float
    balanced_accuracy: float
    positive_rate: float
    avg_future_return: float
    strategy_return: float
    buy_and_hold_return: float


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def standardize(
    train_x: np.ndarray, validation_x: np.ndarray, test_x: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = train_x.mean(axis=0, keepdims=True)
    std = train_x.std(axis=0, keepdims=True)
    std = np.where(std < 1e-6, 1.0, std)
    return (
        (train_x - mean) / std,
        (validation_x - mean) / std,
        (test_x - mean) / std,
    )


def sigmoid(values: np.ndarray) -> np.ndarray:
    clipped = np.clip(values, -30.0, 30.0)
    return 1.0 / (1.0 + np.exp(-clipped))


def add_bias(features: np.ndarray) -> np.ndarray:
    return np.concatenate([features, np.ones((features.shape[0], 1), dtype=features.dtype)], axis=1)


def add_interaction_terms(
    train_x: np.ndarray, validation_x: np.ndarray, test_x: np.ndarray, feature_names: list[str]
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    feature_index = {name: idx for idx, name in enumerate(feature_names)}
    configured_pairs = get_env_interaction_pairs("AR_EXTRA_INTERACTIONS", INTERACTION_FEATURE_PAIRS)
    interaction_pairs = [
        (feature_index[left], feature_index[right])
        for left, right in configured_pairs
        if left in feature_index and right in feature_index
    ]

    def augment(features: np.ndarray) -> np.ndarray:
        extras = [features[:, i : i + 1] * features[:, j : j + 1] for i, j in interaction_pairs]
        return np.concatenate([features] + extras, axis=1)

    return augment(train_x), augment(validation_x), augment(test_x)


def build_derived_feature_column(frame, name: str) -> np.ndarray:
    eps = 1e-6
    open_price = frame["open"].to_numpy(dtype=np.float32)
    high_price = frame["high"].to_numpy(dtype=np.float32)
    low_price = frame["low"].to_numpy(dtype=np.float32)
    close_price = frame["close"].to_numpy(dtype=np.float32)
    ret_1 = frame["ret_1"].to_numpy(dtype=np.float32)
    range_size = np.maximum(high_price - low_price, eps)
    body_size = close_price - open_price
    prev_close = close_price / np.maximum(1.0 + ret_1, eps)

    if name == "intraday_return":
        return body_size / np.maximum(open_price, eps)
    if name == "upper_shadow":
        return (high_price - np.maximum(open_price, close_price)) / np.maximum(close_price, eps)
    if name == "lower_shadow":
        return (np.minimum(open_price, close_price) - low_price) / np.maximum(close_price, eps)
    if name == "close_location":
        return (close_price - low_price) / range_size - 0.5
    if name == "overnight_gap":
        return open_price / np.maximum(prev_close, eps) - 1.0
    if name == "body_to_range":
        return body_size / range_size
    raise ValueError(f"Unsupported derived feature: {name}")


def assemble_feature_matrices(
    splits: dict[str, object],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    feature_names = list(FEATURE_COLUMNS)
    for column in EXTRA_FEATURE_COLUMNS:
        if column in splits["train"].frame.columns:
            feature_names.append(column)
    for column in get_env_csv("AR_EXTRA_BASE_FEATURES", ()):
        if column in splits["train"].frame.columns and column not in feature_names:
            feature_names.append(column)
    drop_features = set(get_env_csv("AR_DROP_FEATURES", DROP_FEATURE_COLUMNS))
    feature_names = [name for name in feature_names if name not in drop_features]

    derived_feature_names = list(get_env_csv("AR_DERIVED_FEATURES", DERIVED_FEATURE_COLUMNS))

    def assemble_split(frame) -> np.ndarray:
        columns = [frame[feature_names].to_numpy(dtype=np.float32)]
        for name in derived_feature_names:
            columns.append(build_derived_feature_column(frame, name).reshape(-1, 1))
        return np.concatenate(columns, axis=1)

    return (
        assemble_split(splits["train"].frame),
        assemble_split(splits["validation"].frame),
        assemble_split(splits["test"].frame),
        feature_names + derived_feature_names,
    )


def logistic_loss(features: np.ndarray, labels: np.ndarray, weights: np.ndarray, l2_reg: float) -> float:
    logits = features @ weights
    probs = sigmoid(logits)
    eps = 1e-8
    ce = -(labels * np.log(probs + eps) + (1.0 - labels) * np.log(1.0 - probs + eps)).mean()
    return float(ce + 0.5 * l2_reg * np.sum(weights[:-1] ** 2))


def get_env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value is not None else default


def get_env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value is not None else default


def get_env_str(name: str, default: str) -> str:
    value = os.getenv(name)
    return value if value is not None else default


def get_env_csv(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return tuple(part.strip() for part in value.split(",") if part.strip())


def get_env_interaction_pairs(
    name: str, default: tuple[tuple[str, str], ...]
) -> tuple[tuple[str, str], ...]:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    pairs = list(default)
    for part in value.split(","):
        left, sep, right = part.strip().partition(":")
        if sep and left and right:
            candidate = (left.strip(), right.strip())
            if candidate not in pairs:
                pairs.append(candidate)
    return tuple(pairs)


def classification_stats(probabilities: np.ndarray, labels: np.ndarray, threshold: float) -> tuple[float, float, float, float, np.ndarray]:
    predictions = (probabilities >= threshold).astype(np.float32)
    tp = float(((predictions == 1) & (labels == 1)).sum())
    tn = float(((predictions == 0) & (labels == 0)).sum())
    fp = float(((predictions == 1) & (labels == 0)).sum())
    fn = float(((predictions == 0) & (labels == 1)).sum())
    return tp, tn, fp, fn, predictions


def select_threshold(probabilities: np.ndarray, labels: np.ndarray, objective: str, threshold_min: float, threshold_max: float, threshold_steps: int) -> float:
    best_threshold = 0.5
    best_primary = -1.0
    best_secondary = -1.0
    for threshold in np.linspace(threshold_min, threshold_max, threshold_steps):
        tp, tn, fp, fn, _ = classification_stats(probabilities, labels, float(threshold))
        precision = tp / max(tp + fp, 1.0)
        recall = tp / max(tp + fn, 1.0)
        specificity = tn / max(tn + fp, 1.0)
        f1 = 2 * precision * recall / max(precision + recall, 1e-8)
        balanced_accuracy = 0.5 * (recall + specificity)
        if objective == "balanced_accuracy":
            primary = balanced_accuracy
            secondary = f1
        else:
            primary = f1
            secondary = balanced_accuracy
        if (
            primary > best_primary
            or (abs(primary - best_primary) < 1e-8 and secondary > best_secondary)
            or (abs(primary - best_primary) < 1e-8 and abs(secondary - best_secondary) < 1e-8 and abs(threshold - 0.5) < abs(best_threshold - 0.5))
        ):
            best_threshold = float(threshold)
            best_primary = primary
            best_secondary = secondary
    return best_threshold


def compute_metrics(
    logits: np.ndarray, labels: np.ndarray, future_returns: np.ndarray, threshold: float = 0.5
) -> Metrics:
    probabilities = sigmoid(logits)
    tp, tn, fp, fn, predictions = classification_stats(probabilities, labels, threshold)
    correct = float((predictions == labels).mean())

    precision = tp / max(tp + fp, 1.0)
    recall = tp / max(tp + fn, 1.0)
    specificity = tn / max(tn + fp, 1.0)
    f1 = 2 * precision * recall / max(precision + recall, 1e-8)
    balanced_accuracy = 0.5 * (recall + specificity)

    strategy_returns = predictions * future_returns
    strategy_compound = float(np.prod(1.0 + strategy_returns) - 1.0)
    buy_and_hold_compound = float(np.prod(1.0 + future_returns) - 1.0)

    eps = 1e-8
    loss = float(
        -(labels * np.log(probabilities + eps) + (1.0 - labels) * np.log(1.0 - probabilities + eps)).mean()
    )
    return Metrics(
        loss=loss,
        accuracy=correct,
        precision=precision,
        recall=recall,
        f1=f1,
        balanced_accuracy=balanced_accuracy,
        positive_rate=float(predictions.mean()),
        avg_future_return=float(np.mean(future_returns)),
        strategy_return=strategy_compound,
        buy_and_hold_return=buy_and_hold_compound,
    )


def main() -> None:
    set_seed(SEED)
    learning_rate = get_env_float("AR_LEARNING_RATE", LEARNING_RATE)
    l2_reg = get_env_float("AR_L2_REG", L2_REG)
    max_epochs = get_env_int("AR_MAX_EPOCHS", MAX_EPOCHS)
    patience = get_env_int("AR_PATIENCE", PATIENCE)
    pos_weight = get_env_float("AR_POS_WEIGHT", POS_WEIGHT)
    neg_weight = get_env_float("AR_NEG_WEIGHT", NEG_WEIGHT)
    threshold_objective = get_env_str("AR_THRESHOLD_OBJECTIVE", THRESHOLD_OBJECTIVE)
    threshold_min = get_env_float("AR_THRESHOLD_MIN", THRESHOLD_MIN)
    threshold_max = get_env_float("AR_THRESHOLD_MAX", THRESHOLD_MAX)
    threshold_steps = get_env_int("AR_THRESHOLD_STEPS", THRESHOLD_STEPS)

    splits = load_splits()
    train_x, validation_x, test_x, feature_names = assemble_feature_matrices(splits)
    train_y = splits["train"].labels
    validation_y = splits["validation"].labels
    test_y = splits["test"].labels

    train_x, validation_x, test_x = standardize(train_x, validation_x, test_x)
    train_x, validation_x, test_x = add_interaction_terms(train_x, validation_x, test_x, feature_names)
    train_x = add_bias(train_x)
    validation_x = add_bias(validation_x)
    test_x = add_bias(test_x)

    weights = np.zeros(train_x.shape[1], dtype=np.float32)
    best_weights = weights.copy()
    best_validation_f1 = -math.inf
    best_epoch = -1
    epochs_without_improvement = 0
    best_threshold = 0.5

    for epoch in range(1, max_epochs + 1):
        logits = train_x @ weights
        probs = sigmoid(logits)
        sample_weights = np.where(train_y == 1.0, pos_weight, neg_weight).astype(np.float32)
        gradient = train_x.T @ ((probs - train_y) * sample_weights) / train_x.shape[0]
        gradient[:-1] += l2_reg * weights[:-1]
        weights -= learning_rate * gradient

        validation_logits = validation_x @ weights
        validation_probs = sigmoid(validation_logits)
        candidate_threshold = select_threshold(
            validation_probs,
            validation_y,
            objective=threshold_objective,
            threshold_min=threshold_min,
            threshold_max=threshold_max,
            threshold_steps=threshold_steps,
        )
        validation_metrics = compute_metrics(
            validation_logits,
            validation_y,
            splits["validation"].frame["future_return"].to_numpy(dtype=np.float32),
            threshold=candidate_threshold,
        )
        if validation_metrics.f1 > best_validation_f1:
            best_validation_f1 = validation_metrics.f1
            best_epoch = epoch
            best_weights = weights.copy()
            best_threshold = candidate_threshold
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1

        if epochs_without_improvement >= patience:
            break

    train_logits = train_x @ best_weights
    validation_logits = validation_x @ best_weights
    test_logits = test_x @ best_weights

    train_metrics = compute_metrics(
        train_logits,
        train_y,
        splits["train"].frame["future_return"].to_numpy(dtype=np.float32),
        threshold=best_threshold,
    )
    validation_metrics = compute_metrics(
        validation_logits,
        validation_y,
        splits["validation"].frame["future_return"].to_numpy(dtype=np.float32),
        threshold=best_threshold,
    )
    test_metrics = compute_metrics(
        test_logits,
        test_y,
        splits["test"].frame["future_return"].to_numpy(dtype=np.float32),
        threshold=best_threshold,
    )

    print("---")
    print(f"task:                 GLD_{HORIZON_DAYS}d_direction")
    print(f"target_column:        {TARGET_COLUMN}")
    print(f"model:                logistic_regression")
    print(f"features:             {len(feature_names)}")
    print(f"learning_rate:        {learning_rate}")
    print(f"l2_reg:               {l2_reg}")
    print(f"pos_weight:           {pos_weight}")
    print(f"neg_weight:           {neg_weight}")
    print(f"threshold_objective:  {threshold_objective}")
    print(f"decision_threshold:   {best_threshold:.3f}")
    print(f"best_epoch:           {best_epoch}")
    print(f"train_loss:           {logistic_loss(train_x, train_y, best_weights, l2_reg):.4f}")
    print(f"train_accuracy:       {train_metrics.accuracy:.4f}")
    print(f"validation_accuracy:  {validation_metrics.accuracy:.4f}")
    print(f"validation_f1:        {validation_metrics.f1:.4f}")
    print(f"validation_bal_acc:   {validation_metrics.balanced_accuracy:.4f}")
    print(f"test_accuracy:        {test_metrics.accuracy:.4f}")
    print(f"test_f1:              {test_metrics.f1:.4f}")
    print(f"test_bal_acc:         {test_metrics.balanced_accuracy:.4f}")
    print(f"test_precision:       {test_metrics.precision:.4f}")
    print(f"test_recall:          {test_metrics.recall:.4f}")
    print(f"test_positive_rate:   {test_metrics.positive_rate:.4f}")
    print(f"test_strategy_return: {test_metrics.strategy_return:.4%}")
    print(f"test_buy_hold_return: {test_metrics.buy_and_hold_return:.4%}")


if __name__ == "__main__":
    main()
