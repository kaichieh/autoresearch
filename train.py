"""
Train a simple GLD 3-day direction classifier.

The goal is not to predict the exact price. We only predict whether GLD
will close higher or lower three trading days from now.

Usage:
    python train.py
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

import numpy as np

from prepare import FEATURE_COLUMNS, HORIZON_DAYS, TARGET_COLUMN, load_splits

SEED = 42
LEARNING_RATE = 0.05
L2_REG = 1e-3
MAX_EPOCHS = 1200
PATIENCE = 120


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


def logistic_loss(features: np.ndarray, labels: np.ndarray, weights: np.ndarray, l2_reg: float) -> float:
    logits = features @ weights
    probs = sigmoid(logits)
    eps = 1e-8
    ce = -(labels * np.log(probs + eps) + (1.0 - labels) * np.log(1.0 - probs + eps)).mean()
    return float(ce + 0.5 * l2_reg * np.sum(weights[:-1] ** 2))


def compute_metrics(
    logits: np.ndarray, labels: np.ndarray, future_returns: np.ndarray
) -> Metrics:
    probabilities = sigmoid(logits)
    predictions = (probabilities >= 0.5).astype(np.float32)

    correct = float((predictions == labels).mean())
    tp = float(((predictions == 1) & (labels == 1)).sum())
    tn = float(((predictions == 0) & (labels == 0)).sum())
    fp = float(((predictions == 1) & (labels == 0)).sum())
    fn = float(((predictions == 0) & (labels == 1)).sum())

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

    splits = load_splits()
    train_x = splits["train"].features
    validation_x = splits["validation"].features
    test_x = splits["test"].features
    train_y = splits["train"].labels
    validation_y = splits["validation"].labels
    test_y = splits["test"].labels

    train_x, validation_x, test_x = standardize(train_x, validation_x, test_x)
    train_x = add_bias(train_x)
    validation_x = add_bias(validation_x)
    test_x = add_bias(test_x)

    weights = np.zeros(train_x.shape[1], dtype=np.float32)
    best_weights = weights.copy()
    best_validation_f1 = -math.inf
    best_epoch = -1
    epochs_without_improvement = 0

    for epoch in range(1, MAX_EPOCHS + 1):
        logits = train_x @ weights
        probs = sigmoid(logits)
        gradient = train_x.T @ (probs - train_y) / train_x.shape[0]
        gradient[:-1] += L2_REG * weights[:-1]
        weights -= LEARNING_RATE * gradient

        validation_logits = validation_x @ weights
        validation_metrics = compute_metrics(
            validation_logits,
            validation_y,
            splits["validation"].frame["future_return"].to_numpy(dtype=np.float32),
        )
        if validation_metrics.f1 > best_validation_f1:
            best_validation_f1 = validation_metrics.f1
            best_epoch = epoch
            best_weights = weights.copy()
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1

        if epochs_without_improvement >= PATIENCE:
            break

    train_logits = train_x @ best_weights
    validation_logits = validation_x @ best_weights
    test_logits = test_x @ best_weights

    train_metrics = compute_metrics(
        train_logits,
        train_y,
        splits["train"].frame["future_return"].to_numpy(dtype=np.float32),
    )
    validation_metrics = compute_metrics(
        validation_logits,
        validation_y,
        splits["validation"].frame["future_return"].to_numpy(dtype=np.float32),
    )
    test_metrics = compute_metrics(
        test_logits,
        test_y,
        splits["test"].frame["future_return"].to_numpy(dtype=np.float32),
    )

    print("---")
    print(f"task:                 GLD_{HORIZON_DAYS}d_direction")
    print(f"target_column:        {TARGET_COLUMN}")
    print(f"model:                logistic_regression")
    print(f"features:             {len(FEATURE_COLUMNS)}")
    print(f"learning_rate:        {LEARNING_RATE}")
    print(f"l2_reg:               {L2_REG}")
    print(f"best_epoch:           {best_epoch}")
    print(f"train_loss:           {logistic_loss(train_x, train_y, best_weights, L2_REG):.4f}")
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
