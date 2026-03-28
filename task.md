# Research Backlog

## Feature Replacement

- [x] Replace `ret_3` with `close_location` and record full metrics. Performance: `validation_f1=0.7100`, `validation_bal_acc=0.5360`, `test_f1=0.6983`.
- [x] Replace `ret_5` with `close_location` and record full metrics. Performance: `validation_f1=0.7070`, `validation_bal_acc=0.5373`, `test_f1=0.6748`.
- [x] Replace `ret_10` with `close_location` and record full metrics. Performance: `validation_f1=0.7114`, `validation_bal_acc=0.5338`, `test_f1=0.7041`.
- [x] Replace `ret_20` with `close_location` and record full metrics. Performance: `validation_f1=0.7099`, `validation_bal_acc=0.5279`, `test_f1=0.6975`.
- [x] Replace `sma_gap_5` with `close_location` and record full metrics. Performance: `validation_f1=0.7154`, `validation_bal_acc=0.5468`, `test_f1=0.6871`.
- [x] Replace `sma_gap_10` with `close_location` and record full metrics. Performance: `validation_f1=0.7137`, `validation_bal_acc=0.5443`, `test_f1=0.6825`.
- [x] Replace `sma_gap_20` with `close_location` and record full metrics. Performance: `validation_f1=0.7109`, `validation_bal_acc=0.5340`, `test_f1=0.7020`.
- [x] Replace `volatility_5` with `close_location` and record full metrics. Performance: `validation_f1=0.7084`, `validation_bal_acc=0.5351`, `test_f1=0.6852`.
- [x] Replace `volatility_10` with `close_location` and record full metrics. Performance: `validation_f1=0.7124`, `validation_bal_acc=0.5415`, `test_f1=0.6862`.
- [x] Replace `range_pct` with `close_location` and record full metrics. Performance: `validation_f1=0.7144`, `validation_bal_acc=0.5407`, `test_f1=0.7030`.
- [x] Replace `ret_3` with `upper_shadow` and record full metrics. Performance: `validation_f1=0.7113`, `validation_bal_acc=0.5404`, `test_f1=0.6861`.
- [x] Replace `ret_5` with `upper_shadow` and record full metrics. Performance: `validation_f1=0.7069`, `validation_bal_acc=0.5357`, `test_f1=0.6755`.
- [x] Replace `ret_10` with `upper_shadow` and record full metrics. Performance: `validation_f1=0.7129`, `validation_bal_acc=0.5413`, `test_f1=0.6865`.
- [x] Replace `ret_20` with `upper_shadow` and record full metrics. Performance: `validation_f1=0.7097`, `validation_bal_acc=0.5313`, `test_f1=0.6929`.
- [x] Replace `range_pct` with `upper_shadow` and record full metrics. Performance: `validation_f1=0.7165`, `validation_bal_acc=0.5480`, `test_f1=0.6849`.
- [x] Replace `ret_3` with `lower_shadow` and record full metrics. Performance: `validation_f1=0.7118`, `validation_bal_acc=0.5402`, `test_f1=0.6933`.
- [x] Replace `ret_5` with `lower_shadow` and record full metrics. Performance: `validation_f1=0.7073`, `validation_bal_acc=0.5339`, `test_f1=0.6808`.
- [x] Replace `ret_10` with `lower_shadow` and record full metrics. Performance: `validation_f1=0.7121`, `validation_bal_acc=0.5368`, `test_f1=0.6937`.
- [x] Replace `ret_20` with `lower_shadow` and record full metrics. Performance: `validation_f1=0.7091`, `validation_bal_acc=0.5299`, `test_f1=0.6951`.
- [x] Replace `range_pct` with `lower_shadow` and record full metrics. Performance: `validation_f1=0.7164`, `validation_bal_acc=0.5464`, `test_f1=0.6921`.
- [x] Replace `ret_3` with `body_to_range` and record full metrics. Performance: `validation_f1=0.7115`, `validation_bal_acc=0.5354`, `test_f1=0.6926`.
- [x] Replace `ret_5` with `body_to_range` and record full metrics. Performance: `validation_f1=0.7081`, `validation_bal_acc=0.5385`, `test_f1=0.6795`.
- [x] Replace `ret_10` with `body_to_range` and record full metrics. Performance: `validation_f1=0.7119`, `validation_bal_acc=0.5336`, `test_f1=0.7041`.
- [x] Replace `ret_20` with `body_to_range` and record full metrics. Performance: `validation_f1=0.7075`, `validation_bal_acc=0.5208`, `test_f1=0.7050`.
- [x] Replace `range_pct` with `body_to_range` and record full metrics. Performance: `validation_f1=0.7155`, `validation_bal_acc=0.5419`, `test_f1=0.7026`.

## Default Feature Inclusion

- [x] Add `close_location` to default features without replacement and retune threshold. Performance: `validation_f1=0.7134`, `validation_bal_acc=0.5477`, `test_f1=0.6860`.
- [x] Add `upper_shadow` to default features without replacement and retune threshold. Performance: `validation_f1=0.7151`, `validation_bal_acc=0.5437`, `test_f1=0.6907`.
- [x] Add `lower_shadow` to default features without replacement and retune threshold. Performance: `validation_f1=0.7147`, `validation_bal_acc=0.5439`, `test_f1=0.6889`.
- [x] Add `body_to_range` to default features without replacement and retune threshold. Performance: `validation_f1=0.7144`, `validation_bal_acc=0.5407`, `test_f1=0.6931`.
- [x] Add `price_z_20` to default features without replacement and retune threshold. Performance: `validation_f1=0.7127`, `validation_bal_acc=0.5381`, `test_f1=0.6937`.
- [x] Add `volume_z_20` to default features without replacement and retune threshold. Performance: `validation_f1=0.7133`, `validation_bal_acc=0.5395`, `test_f1=0.6888`.
- [x] Add `trend_score_3_5_10` to default features without replacement and retune threshold. Performance: `validation_f1=0.7122`, `validation_bal_acc=0.5384`, `test_f1=0.6949`.
- [x] Add `trend_agree_3_5_10` to default features without replacement and retune threshold. Performance: `validation_f1=0.7147`, `validation_bal_acc=0.5439`, `test_f1=0.6893`.
- [x] Add `close_location`, `upper_shadow`, and `lower_shadow` together as default candlestick context. Performance: `validation_f1=0.7119`, `validation_bal_acc=0.5336`, `test_f1=0.7013`.
- [x] Add all four new `prepare.py` features together and test whether joint inclusion helps. Performance: `validation_f1=0.7078`, `validation_bal_acc=0.5255`, `test_f1=0.7064`.

## Interaction Search

- [x] Test `close_location:volume_vs_20`. Performance: `validation_f1=0.7133`, `validation_bal_acc=0.5527`, `test_f1=0.6767`.
- [x] Test `close_location:drawdown_20`. Performance: `validation_f1=0.7161`, `validation_bal_acc=0.5432`, `test_f1=0.6903`.
- [x] Test `close_location:breakout_20`. Performance: `validation_f1=0.7134`, `validation_bal_acc=0.5411`, `test_f1=0.6880`.
- [x] Test `close_location:rsi_14`. Performance: `validation_f1=0.7083`, `validation_bal_acc=0.5335`, `test_f1=0.6997`.
- [x] Test `close_location:intraday_return`. Performance: `validation_f1=0.7127`, `validation_bal_acc=0.5381`, `test_f1=0.7037`.
- [x] Test `close_location:overnight_gap`. Performance: `validation_f1=0.7134`, `validation_bal_acc=0.5477`, `test_f1=0.6860`.
- [x] Test `upper_shadow:volume_vs_20`. Performance: `validation_f1=0.7136`, `validation_bal_acc=0.5427`, `test_f1=0.6861`.
- [x] Test `upper_shadow:drawdown_20`. Performance: `validation_f1=0.7128`, `validation_bal_acc=0.5397`, `test_f1=0.6888`.
- [x] Test `upper_shadow:breakout_20`. Performance: `validation_f1=0.7118`, `validation_bal_acc=0.5402`, `test_f1=0.6843`.
- [x] Test `upper_shadow:rsi_14`. Performance: `validation_f1=0.7084`, `validation_bal_acc=0.5269`, `test_f1=0.6981`.
- [x] Test `lower_shadow:volume_vs_20`. Performance: `validation_f1=0.7142`, `validation_bal_acc=0.5441`, `test_f1=0.6866`.
- [x] Test `lower_shadow:drawdown_20`. Performance: `validation_f1=0.7126`, `validation_bal_acc=0.5366`, `test_f1=0.6978`.
- [x] Test `lower_shadow:breakout_20`. Performance: `validation_f1=0.7147`, `validation_bal_acc=0.5439`, `test_f1=0.6895`.
- [x] Test `lower_shadow:rsi_14`. Performance: `validation_f1=0.7101`, `validation_bal_acc=0.5295`, `test_f1=0.7047`.
- [x] Test `body_to_range:volume_vs_20`. Performance: `validation_f1=0.7124`, `validation_bal_acc=0.5334`, `test_f1=0.7046`.
- [x] Test `body_to_range:drawdown_20`. Performance: `validation_f1=0.7159`, `validation_bal_acc=0.5466`, `test_f1=0.6859`.
- [x] Test `body_to_range:breakout_20`. Performance: `validation_f1=0.7145`, `validation_bal_acc=0.5423`, `test_f1=0.6910`.
- [x] Test `body_to_range:rsi_14`. Performance: `validation_f1=0.7099`, `validation_bal_acc=0.5344`, `test_f1=0.7021`.
- [x] Test `price_z_20:volume_z_20`. Performance: `validation_f1=0.7108`, `validation_bal_acc=0.5324`, `test_f1=0.6920`.
- [x] Test `price_z_20:volume_vs_20`. Performance: `validation_f1=0.7127`, `validation_bal_acc=0.5381`, `test_f1=0.6943`.
- [x] Test `price_z_20:drawdown_20`. Performance: `validation_f1=0.7099`, `validation_bal_acc=0.5279`, `test_f1=0.7079`.
- [x] Test `price_z_20:breakout_20`. Performance: `validation_f1=0.7116`, `validation_bal_acc=0.5370`, `test_f1=0.6912`.
- [x] Test `volume_z_20:breakout_20`. Performance: `validation_f1=0.7134`, `validation_bal_acc=0.5411`, `test_f1=0.6837`.
- [x] Test `volume_z_20:drawdown_20`. Performance: `validation_f1=0.7132`, `validation_bal_acc=0.5379`, `test_f1=0.6911`.
- [x] Test `trend_score_3_5_10:volume_vs_20`. Performance: `validation_f1=0.7122`, `validation_bal_acc=0.5384`, `test_f1=0.6943`.

## Narrow Local Search Around Current Best

- [x] Keep current best features and only add `rsi_14:volume_vs_20`. Performance: `validation_f1=0.7125`, `validation_bal_acc=0.5350`, `test_f1=0.7047`.
- [x] Keep current best features and only add `breakout_20:volume_vs_20`. Performance: `validation_f1=0.7139`, `validation_bal_acc=0.5409`, `test_f1=0.6871`.
- [x] Keep current best features and only add `drawdown_20:intraday_return`. Performance: `validation_f1=0.7131`, `validation_bal_acc=0.5363`, `test_f1=0.6972`.
- [x] Keep current best features and only add `drawdown_20:overnight_gap`. Performance: `validation_f1=0.7104`, `validation_bal_acc=0.5277`, `test_f1=0.7035`.
- [x] Keep current best features and only add `breakout_20:overnight_gap`. Performance: `validation_f1=0.7137`, `validation_bal_acc=0.5443`, `test_f1=0.6850`.
- [x] Keep current best features and only add `breakout_20:intraday_return`. Performance: `validation_f1=0.7140`, `validation_bal_acc=0.5425`, `test_f1=0.6877`.
- [x] Keep current best features and test `neg_weight = 1.25`. Performance: `validation_f1=0.7140`, `validation_bal_acc=0.5425`, `test_f1=0.6860`.
- [x] Keep current best features and test `neg_weight = 1.35`. Performance: `validation_f1=0.7107`, `validation_bal_acc=0.5308`, `test_f1=0.7028`.
- [x] Keep current best features and test `l2_reg = 5e-4`. Performance: `validation_f1=0.7151`, `validation_bal_acc=0.5437`, `test_f1=0.6872`.
- [x] Keep current best features and test `l2_reg = 2e-3`. Performance: `validation_f1=0.7151`, `validation_bal_acc=0.5437`, `test_f1=0.6872`.
- [x] Keep current best features and test `learning_rate = 0.01`. Performance: `validation_f1=0.7154`, `validation_bal_acc=0.5468`, `test_f1=0.6780`.
- [x] Keep current best features and test `learning_rate = 0.03`. Performance: `validation_f1=0.7144`, `validation_bal_acc=0.5407`, `test_f1=0.6975`.
- [x] Keep current best features and test `threshold_steps = 801`. Performance: `validation_f1=0.7153`, `validation_bal_acc=0.5452`, `test_f1=0.6849`.
- [x] Keep current best features and search threshold range `0.35` to `0.65`. Performance: `validation_f1=0.7153`, `validation_bal_acc=0.5452`, `test_f1=0.6849`.
- [x] Keep current best features and search threshold range `0.40` to `0.60`. Performance: `validation_f1=0.7153`, `validation_bal_acc=0.5452`, `test_f1=0.6849`.

## Objective And Guardrail Variants

- [x] Optimize threshold by `balanced_accuracy` and keep model weights unchanged. Performance: `validation_f1=0.7151`, `validation_bal_acc=0.5437`, `test_f1=0.6872`.
- [ ] Optimize threshold by `f1` but require `validation_bal_acc >= 0.54`.
- [ ] Optimize threshold by `f1` but require `validation_bal_acc >= 0.55`.
- [ ] Optimize threshold by `f1` but require `validation_accuracy >= 0.58`.
- [ ] Optimize threshold by `f1` but require `test_positive_rate <= 0.88`.
- [x] Train with `pos_weight = 1.1` and `neg_weight = 1.3`. Performance: `validation_f1=0.7073`, `validation_bal_acc=0.5257`, `test_f1=0.6902`.
- [x] Train with `pos_weight = 1.0` and `neg_weight = 1.2`. Performance: `validation_f1=0.7083`, `validation_bal_acc=0.5335`, `test_f1=0.6886`.
- [x] Train with `pos_weight = 1.0` and `neg_weight = 1.4`. Performance: `validation_f1=0.7073`, `validation_bal_acc=0.5257`, `test_f1=0.7040`.
- [ ] Compare best epoch chosen by `validation_f1` versus best epoch chosen by `validation_bal_acc`.
- [x] Compare threshold selected on validation versus fixed threshold `0.50`. Performance: `validation_f1=0.1612`, `validation_bal_acc=0.5234`, `test_f1=0.1109`.

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

- [x] Run 3-fold walk-forward validation on the current best setup and save fold metrics. Performance: fold `validation_f1=[0.6957, 0.7165, 0.7283]`, mean `validation_f1=0.7135`, mean `validation_bal_acc=0.5238`.
- [x] Run 4-fold walk-forward validation on the current best setup and save fold metrics. Performance: fold `validation_f1=[0.6223, 0.6975, 0.7324, 0.6799]`, mean `validation_f1=0.6830`, mean `validation_bal_acc=0.5087`.
- [x] Compare fold-level thresholds for the current best setup. Performance: 3-fold thresholds `[0.453, 0.497, 0.448]`; 4-fold thresholds `[0.494, 0.498, 0.497, 0.497]`.
- [x] Compare fold-level `validation_f1` variance for the current best setup. Performance: 3-fold variance `0.000182`; 4-fold variance `0.001586`.
- [x] Compare fold-level `validation_bal_acc` variance for the current best setup. Performance: 3-fold variance `0.000295`; 4-fold variance `0.000180`.
- [x] Re-run the current best setup with three random seeds to confirm determinism. Performance: seeds `1/2/3` all matched at `validation_f1=0.7165`, `validation_bal_acc=0.5480`, `test_f1=0.6849`.
- [x] Verify whether the best setup still wins after regenerating the dataset from scratch. Performance: refreshed dataset still gave `validation_f1=0.7165`, `validation_bal_acc=0.5480`, `test_f1=0.6849`.
- [x] Verify whether the best setup still wins when threshold is fixed to `0.50`. Performance: fixed-threshold run fell to `validation_f1=0.1612`, `validation_bal_acc=0.5234`, `test_f1=0.1109`.
- [x] Verify whether the best setup still wins when `threshold_steps = 1601`. Performance: unchanged at `validation_f1=0.7165`, `validation_bal_acc=0.5480`, `test_f1=0.6849`.
- [ ] Summarize which feature families help validation most consistently across time splits.
