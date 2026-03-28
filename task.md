# Research Backlog

## Feature Replacement

- [ ] Replace `ret_3` with `close_location` and record full metrics.
- [ ] Replace `ret_5` with `close_location` and record full metrics.
- [ ] Replace `ret_10` with `close_location` and record full metrics.
- [ ] Replace `ret_20` with `close_location` and record full metrics.
- [ ] Replace `sma_gap_5` with `close_location` and record full metrics.
- [ ] Replace `sma_gap_10` with `close_location` and record full metrics.
- [ ] Replace `sma_gap_20` with `close_location` and record full metrics.
- [ ] Replace `volatility_5` with `close_location` and record full metrics.
- [ ] Replace `volatility_10` with `close_location` and record full metrics.
- [ ] Replace `range_pct` with `close_location` and record full metrics.
- [ ] Replace `ret_3` with `upper_shadow` and record full metrics.
- [ ] Replace `ret_5` with `upper_shadow` and record full metrics.
- [ ] Replace `ret_10` with `upper_shadow` and record full metrics.
- [ ] Replace `ret_20` with `upper_shadow` and record full metrics.
- [ ] Replace `range_pct` with `upper_shadow` and record full metrics.
- [ ] Replace `ret_3` with `lower_shadow` and record full metrics.
- [ ] Replace `ret_5` with `lower_shadow` and record full metrics.
- [ ] Replace `ret_10` with `lower_shadow` and record full metrics.
- [ ] Replace `ret_20` with `lower_shadow` and record full metrics.
- [ ] Replace `range_pct` with `lower_shadow` and record full metrics.
- [ ] Replace `ret_3` with `body_to_range` and record full metrics.
- [ ] Replace `ret_5` with `body_to_range` and record full metrics.
- [ ] Replace `ret_10` with `body_to_range` and record full metrics.
- [ ] Replace `ret_20` with `body_to_range` and record full metrics.
- [ ] Replace `range_pct` with `body_to_range` and record full metrics.

## Default Feature Inclusion

- [ ] Add `close_location` to default features without replacement and retune threshold.
- [ ] Add `upper_shadow` to default features without replacement and retune threshold.
- [ ] Add `lower_shadow` to default features without replacement and retune threshold.
- [ ] Add `body_to_range` to default features without replacement and retune threshold.
- [ ] Add `price_z_20` to default features without replacement and retune threshold.
- [ ] Add `volume_z_20` to default features without replacement and retune threshold.
- [ ] Add `trend_score_3_5_10` to default features without replacement and retune threshold.
- [ ] Add `trend_agree_3_5_10` to default features without replacement and retune threshold.
- [ ] Add `close_location`, `upper_shadow`, and `lower_shadow` together as default candlestick context.
- [ ] Add all four new `prepare.py` features together and test whether joint inclusion helps.

## Interaction Search

- [ ] Test `close_location:volume_vs_20`.
- [ ] Test `close_location:drawdown_20`.
- [ ] Test `close_location:breakout_20`.
- [ ] Test `close_location:rsi_14`.
- [ ] Test `close_location:intraday_return`.
- [ ] Test `close_location:overnight_gap`.
- [ ] Test `upper_shadow:volume_vs_20`.
- [ ] Test `upper_shadow:drawdown_20`.
- [ ] Test `upper_shadow:breakout_20`.
- [ ] Test `upper_shadow:rsi_14`.
- [ ] Test `lower_shadow:volume_vs_20`.
- [ ] Test `lower_shadow:drawdown_20`.
- [ ] Test `lower_shadow:breakout_20`.
- [ ] Test `lower_shadow:rsi_14`.
- [ ] Test `body_to_range:volume_vs_20`.
- [ ] Test `body_to_range:drawdown_20`.
- [ ] Test `body_to_range:breakout_20`.
- [ ] Test `body_to_range:rsi_14`.
- [ ] Test `price_z_20:volume_z_20`.
- [ ] Test `price_z_20:volume_vs_20`.
- [ ] Test `price_z_20:drawdown_20`.
- [ ] Test `price_z_20:breakout_20`.
- [ ] Test `volume_z_20:breakout_20`.
- [ ] Test `volume_z_20:drawdown_20`.
- [ ] Test `trend_score_3_5_10:volume_vs_20`.

## Narrow Local Search Around Current Best

- [ ] Keep current best features and only add `rsi_14:volume_vs_20`.
- [ ] Keep current best features and only add `breakout_20:volume_vs_20`.
- [ ] Keep current best features and only add `drawdown_20:intraday_return`.
- [ ] Keep current best features and only add `drawdown_20:overnight_gap`.
- [ ] Keep current best features and only add `breakout_20:overnight_gap`.
- [ ] Keep current best features and only add `breakout_20:intraday_return`.
- [ ] Keep current best features and test `neg_weight = 1.25`.
- [ ] Keep current best features and test `neg_weight = 1.35`.
- [ ] Keep current best features and test `l2_reg = 5e-4`.
- [ ] Keep current best features and test `l2_reg = 2e-3`.
- [ ] Keep current best features and test `learning_rate = 0.01`.
- [ ] Keep current best features and test `learning_rate = 0.03`.
- [ ] Keep current best features and test `threshold_steps = 801`.
- [ ] Keep current best features and search threshold range `0.35` to `0.65`.
- [ ] Keep current best features and search threshold range `0.40` to `0.60`.

## Objective And Guardrail Variants

- [ ] Optimize threshold by `balanced_accuracy` and keep model weights unchanged.
- [ ] Optimize threshold by `f1` but require `validation_bal_acc >= 0.54`.
- [ ] Optimize threshold by `f1` but require `validation_bal_acc >= 0.55`.
- [ ] Optimize threshold by `f1` but require `validation_accuracy >= 0.58`.
- [ ] Optimize threshold by `f1` but require `test_positive_rate <= 0.88`.
- [ ] Train with `pos_weight = 1.1` and `neg_weight = 1.3`.
- [ ] Train with `pos_weight = 1.0` and `neg_weight = 1.2`.
- [ ] Train with `pos_weight = 1.0` and `neg_weight = 1.4`.
- [ ] Compare best epoch chosen by `validation_f1` versus best epoch chosen by `validation_bal_acc`.
- [ ] Compare threshold selected on validation versus fixed threshold `0.50`.

## Prepare.py Expansion

- [ ] Add `ret_2` as a new short-horizon return feature.
- [ ] Add `ret_15` as an intermediate-horizon return feature.
- [ ] Add `sma_gap_3` as a shorter moving-average gap feature.
- [ ] Add `sma_gap_50` as a longer moving-average gap feature.
- [ ] Add `volatility_3` as a shorter realized-volatility feature.
- [ ] Add `volatility_20` as a longer realized-volatility feature.
- [ ] Add `range_z_20` as a rolling normalized range feature.
- [ ] Add `volume_change_5` as a multi-day volume change feature.
- [ ] Add `volume_vs_5` as a short-window relative volume feature.
- [ ] Add `momentum_gap_3_10` defined from `ret_3 - ret_10`.
- [ ] Add `sma_stack_bullish` to indicate short MA above medium and long MA.
- [ ] Add `inside_bar` candlestick pattern feature.
- [ ] Add `outside_bar` candlestick pattern feature.
- [ ] Add `gap_up_flag` binary feature.
- [ ] Add `gap_down_flag` binary feature.

## Validation And Stability

- [ ] Run 3-fold walk-forward validation on the current best setup and save fold metrics.
- [ ] Run 4-fold walk-forward validation on the current best setup and save fold metrics.
- [ ] Compare fold-level thresholds for the current best setup.
- [ ] Compare fold-level `validation_f1` variance for the current best setup.
- [ ] Compare fold-level `validation_bal_acc` variance for the current best setup.
- [ ] Re-run the current best setup with three random seeds to confirm determinism.
- [ ] Verify whether the best setup still wins after regenerating the dataset from scratch.
- [ ] Verify whether the best setup still wins when threshold is fixed to `0.50`.
- [ ] Verify whether the best setup still wins when `threshold_steps = 1601`.
- [ ] Summarize which feature families help validation most consistently across time splits.
