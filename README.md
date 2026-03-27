# autoresearch-gld

This fork repurposes `autoresearch` into a much smaller and more approachable task:

`Predict whether GLD will be up or down 3 trading days from now.`

Instead of training a language model for five minutes on a GPU, this version downloads daily GLD prices, builds a small tabular dataset, and trains a lightweight binary classifier. The core loop is still similar:

1. prepare data
2. train a baseline
3. modify the experiment code
4. compare validation metrics

## Files That Matter

- `prepare.py`: downloads GLD daily price history and engineers features.
- `train.py`: trains and evaluates the direction classifier.
- `program.md`: the research brief for future agent-driven iteration.

## Task Definition

- Input: daily GLD market features derived from historical prices and volume
- Target: whether `close[t+3] > close[t]`
- Primary metric: validation F1
- Secondary metrics: accuracy, balanced accuracy, and a toy long-only strategy return

This is intentionally a simple benchmark. The goal is fast iteration and easy-to-understand results, not production trading.

## Quick Start

Requirements:

- Python 3.10+
- `uv` or plain Python

Install dependencies:

```bash
uv sync
```

Prepare the dataset:

```bash
uv run prepare.py
```

Train the baseline:

```bash
uv run train.py
```

## Design Notes

- Splits are chronological, not shuffled.
- Features use only information known at prediction time.
- `validation_f1` is the selection metric.
- The reported strategy return is only a toy sanity check, not an investable backtest.

## Ideas For Future Experiments

- swap the MLP for logistic regression
- tune thresholds using validation F1
- add richer momentum or volatility features
- compare GLD with spot gold proxies or macro features
- add walk-forward evaluation instead of one fixed split

## Disclaimer

This project is for experimentation and learning. It is not financial advice, and the metrics here are far too simple for real trading decisions.
