# Next Tasks

- [ ] 直接加入 `close_location` 進預設並做 feature replacement。
- [ ] 試新的 `objective` / `guardrail` 組合，重新平衡 `validation_f1` 和 `validation_bal_acc`。
- [ ] 擴到 `prepare.py` 增加真正新的時間序列特徵。
- [ ] 把 `upper_shadow` 和 `lower_shadow` 納入預設候選，做系統化 feature replacement。
- [ ] 針對 `volume_vs_20` 相關 interaction 做更窄但更深的搜尋。
- [ ] 測試 `close_location` 與 `volume_vs_20`、`drawdown_20` 的新 interaction 組合。
- [ ] 測試 `body_to_range` 是否能替換現有某個短期動能特徵並提升 validation 表現。
- [ ] 在 `prepare.py` 增加 rolling z-score 類價格與成交量特徵。
- [ ] 在 `prepare.py` 增加多視窗趨勢一致性特徵，例如 `ret_3`、`ret_5`、`ret_10` 同向指標。
- [ ] 試 walk-forward validation 或多段 validation，檢查目前最佳設定是否穩定。
