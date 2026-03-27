# autoresearch-gld

This repo is now an experiment in autonomous research for a simple financial prediction task:

`Predict whether GLD will be up or down 3 trading days from now.`

## Scope

The repo keeps the same small shape:

- `prepare.py`: fixed data download and feature engineering for GLD. Do not modify unless the human explicitly asks.
- `train.py`: the main experimental surface. This is where model choice, optimization, thresholds, and training logic can evolve.
- `program.md`: the human-facing research brief.

## Objective

The current target is binary classification:

- label `1`: `close[t+3] > close[t]`
- label `0`: otherwise

Primary metric:

- `validation_f1`

Secondary metrics:

- `validation_accuracy`
- `validation_bal_acc`
- `test_f1`
- `test_strategy_return`

The validation set is the selection metric. The test set is only for reporting after choosing a candidate.

## Rules

- Respect chronological splits. Never shuffle across time.
- Avoid data leakage. Only use information available at day `t` to predict day `t+3`.
- Prefer simple changes over complicated ones when performance is similar.
- Keep the repo lightweight. Do not add unnecessary dependencies.
- If a change makes the model look better by abusing the test set, reject it.

## Good experiment ideas

- Replace the MLP with logistic regression or a wider/deeper network.
- Tune hidden size, learning rate, weight decay, patience, or training epochs.
- Change the decision threshold away from `0.5`.
- Add or remove a few features in `prepare.py` if the human explicitly asks for broader changes.
- Compare optimizing BCE loss versus a threshold chosen to maximize validation F1.

## Bad experiment ideas

- Using future prices inside features.
- Picking a model based on test performance.
- Turning this into exact price regression before the classification baseline is solid.
- Adding lots of complexity with no clear validation improvement.

## Suggested workflow

1. Run `python prepare.py` once to refresh the cached GLD dataset.
2. Run `python train.py` to establish a baseline.
3. Modify `train.py`.
4. Re-run `python train.py`.
5. Keep only changes that improve validation performance or meaningfully simplify the code.
