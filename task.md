# Next Tasks

- [x] Directly add `close_location` to the default set and test feature replacement. Result: `validation_f1 = 0.7101`, did not beat `0.7164`.
- [x] Try new `objective` / `guardrail` combinations to rebalance `validation_f1` and `validation_bal_acc`. Result: balanced-accuracy objective fell to `validation_f1 = 0.6505`.
- [x] Extend `prepare.py` with genuinely new time-series features. Added `price_z_20`, `volume_z_20`, `trend_score_3_5_10`, and `trend_agree_3_5_10`.
- [x] Add `upper_shadow` and `lower_shadow` into the default candidate pool and run systematic replacement tests. Result: `validation_f1 = 0.7140`, still below best.
- [x] Run a narrower but deeper search around `volume_vs_20` interactions. Completed; current best still comes from this line at `validation_f1 = 0.7164`.
- [x] Test new `close_location` interactions with `volume_vs_20` and `drawdown_20`. Result: `validation_f1 = 0.7133`, no breakthrough.
- [x] Test whether `body_to_range` can replace an existing short-horizon momentum feature. Result: `validation_f1 = 0.7111`, no breakthrough.
- [x] Add rolling z-score style price and volume features in `prepare.py`. Result: added `price_z_20` and `volume_z_20`; test reached `validation_f1 = 0.7108`.
- [x] Add multi-window trend-consistency features in `prepare.py`. Result: added `trend_score_3_5_10` and `trend_agree_3_5_10`; test reached `validation_f1 = 0.7143`.
- [x] Run walk-forward or multi-segment validation to check whether the current best setup is stable. Result: 3-fold chronological walk-forward mean `validation_f1 = 0.7131`, min `0.6957`, mean `validation_bal_acc = 0.5224`.
