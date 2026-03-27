# autoresearch-gld

This repo is now an experiment in autonomous research for a simple financial prediction task:

`Predict whether GLD will be up or down 3 trading days from now.`

## Scope

The repo keeps the same small shape:

- `prepare.py`: fixed data download and feature engineering for GLD. Do not modify unless the human explicitly asks.
- `train.py`: the main experimental surface. This is where model choice, optimization, thresholds, and training logic can evolve.
- `program.md`: the human-facing research brief.
- `results.tsv`: tab-separated experiment log for comparing runs by commit.

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
5. Append the new metrics to `results.tsv` with the current commit SHA and a short description.
6. Keep only changes that improve validation performance or meaningfully simplify the code.

## Autonomous Loop

Once the experiment loop begins, do not stop to ask the human whether to continue. Keep running experiments until explicitly interrupted.

LOOP FOREVER:

1. Look at the git state: the current branch and commit we are on.
2. Tune `train.py` with one concrete experimental idea by directly hacking the code.
3. `git commit`
4. Run the experiment and redirect output to a log file:
   `python train.py > run.log 2>&1`
   Do not use `tee`, and do not flood the conversation with full training output.
5. Read out the key metrics from `run.log`.
   At minimum inspect:
   `validation_f1`
   `validation_accuracy`
   `validation_bal_acc`
   `test_f1`
   `test_accuracy`
   `test_bal_acc`
6. If the expected metrics are missing, treat the run as a crash.
   Read the end of `run.log`, diagnose the failure, and try a small fix.
   If the idea still fails after a few attempts, give up on that idea.
7. Record the result in `results.tsv`.
8. If `validation_f1` improved, advance the branch and keep the commit.
9. If `validation_f1` is equal or worse, reset back to where the experiment started and move on to the next idea.

The primary selection metric is still `validation_f1`. Use `validation_bal_acc` as an important guardrail so the model does not collapse into predicting almost all ups or almost all downs.

## results.tsv format

Use these columns:

```tsv
commit	validation_f1	validation_accuracy	validation_bal_acc	test_f1	test_accuracy	test_bal_acc	status	description
```

- `commit`: short git SHA
- `validation_f1`: primary selection metric
- `validation_accuracy`: secondary metric
- `validation_bal_acc`: secondary metric that helps detect one-sided predictors
- `test_f1`: report-only metric after choosing a candidate
- `test_accuracy`: report-only metric
- `test_bal_acc`: report-only metric
- `status`: usually `keep`, `discard`, or `baseline`
- `description`: short summary of what changed
