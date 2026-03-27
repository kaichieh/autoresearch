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
import torch
import torch.nn as nn

from prepare import FEATURE_COLUMNS, HORIZON_DAYS, TARGET_COLUMN, load_splits

SEED = 42
HIDDEN_DIM = 32
LEARNING_RATE = 1e-3
WEIGHT_DECAY = 1e-4
MAX_EPOCHS = 400
PATIENCE = 40


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


class DirectionClassifier(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.network(features).squeeze(-1)


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


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


def to_tensor(array: np.ndarray, device: torch.device) -> torch.Tensor:
    return torch.tensor(array, dtype=torch.float32, device=device)


def compute_classification_metrics(
    logits: torch.Tensor, labels: torch.Tensor, future_returns: np.ndarray
) -> Metrics:
    probabilities = torch.sigmoid(logits)
    predictions = (probabilities >= 0.5).float()

    correct = (predictions == labels).float().mean().item()
    tp = ((predictions == 1) & (labels == 1)).sum().item()
    tn = ((predictions == 0) & (labels == 0)).sum().item()
    fp = ((predictions == 1) & (labels == 0)).sum().item()
    fn = ((predictions == 0) & (labels == 1)).sum().item()

    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    specificity = tn / max(tn + fp, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-8)
    balanced_accuracy = 0.5 * (recall + specificity)

    strategy_signal = predictions.detach().cpu().numpy().astype(np.float32)
    strategy_returns = strategy_signal * future_returns
    strategy_compound = float(np.prod(1.0 + strategy_returns) - 1.0)
    buy_and_hold_compound = float(np.prod(1.0 + future_returns) - 1.0)

    loss = nn.functional.binary_cross_entropy_with_logits(logits, labels).item()
    return Metrics(
        loss=loss,
        accuracy=correct,
        precision=precision,
        recall=recall,
        f1=f1,
        balanced_accuracy=balanced_accuracy,
        positive_rate=predictions.mean().item(),
        avg_future_return=float(np.mean(future_returns)),
        strategy_return=strategy_compound,
        buy_and_hold_return=buy_and_hold_compound,
    )


def evaluate(
    model: nn.Module,
    features: torch.Tensor,
    labels: torch.Tensor,
    future_returns: np.ndarray,
) -> Metrics:
    model.eval()
    with torch.no_grad():
        logits = model(features)
    return compute_classification_metrics(logits, labels, future_returns)


def main() -> None:
    set_seed(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    splits = load_splits()
    train_x = splits["train"].features
    validation_x = splits["validation"].features
    test_x = splits["test"].features
    train_y = splits["train"].labels
    validation_y = splits["validation"].labels
    test_y = splits["test"].labels

    train_x, validation_x, test_x = standardize(train_x, validation_x, test_x)

    train_features = to_tensor(train_x, device)
    validation_features = to_tensor(validation_x, device)
    test_features = to_tensor(test_x, device)
    train_labels = to_tensor(train_y, device)
    validation_labels = to_tensor(validation_y, device)
    test_labels = to_tensor(test_y, device)

    model = DirectionClassifier(input_dim=train_features.shape[1], hidden_dim=HIDDEN_DIM).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    loss_fn = nn.BCEWithLogitsLoss()

    best_state = None
    best_validation_f1 = -math.inf
    best_epoch = -1
    epochs_without_improvement = 0

    for epoch in range(1, MAX_EPOCHS + 1):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        logits = model(train_features)
        loss = loss_fn(logits, train_labels)
        loss.backward()
        optimizer.step()

        validation_metrics = evaluate(
            model,
            validation_features,
            validation_labels,
            splits["validation"].frame["future_return"].to_numpy(dtype=np.float32),
        )
        if validation_metrics.f1 > best_validation_f1:
            best_validation_f1 = validation_metrics.f1
            best_epoch = epoch
            best_state = {name: tensor.detach().cpu().clone() for name, tensor in model.state_dict().items()}
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1

        if epochs_without_improvement >= PATIENCE:
            break

    if best_state is None:
        raise RuntimeError("Training did not produce a valid checkpoint.")

    model.load_state_dict(best_state)
    model.to(device)

    train_metrics = evaluate(
        model,
        train_features,
        train_labels,
        splits["train"].frame["future_return"].to_numpy(dtype=np.float32),
    )
    validation_metrics = evaluate(
        model,
        validation_features,
        validation_labels,
        splits["validation"].frame["future_return"].to_numpy(dtype=np.float32),
    )
    test_metrics = evaluate(
        model,
        test_features,
        test_labels,
        splits["test"].frame["future_return"].to_numpy(dtype=np.float32),
    )

    print("---")
    print(f"task:                 GLD_{HORIZON_DAYS}d_direction")
    print(f"target_column:        {TARGET_COLUMN}")
    print(f"device:               {device.type}")
    print(f"features:             {len(FEATURE_COLUMNS)}")
    print(f"hidden_dim:           {HIDDEN_DIM}")
    print(f"learning_rate:        {LEARNING_RATE}")
    print(f"weight_decay:         {WEIGHT_DECAY}")
    print(f"best_epoch:           {best_epoch}")
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
