# Deep Reasoning Duration and Capability Policy

Version: 1.1.0  
Canonical quality model: `CONTINUOUS_THINKING_QUALITY_OS.md` v3.0.0  
Machine-readable profile: `../control-plane/ai-system/configs/continuous-thinking-global.json`

## Purpose

建立高品質深度處理模式，避免快速輸出第一個可行答案造成反覆修改、假完成與低品質修補；同時避免把人為等待時間誤當作深度。

## Deep Reasoning Requirement

對複雜、重要、架構型、研究型、除錯型任務：

- 不應立即輸出第一個 plausible solution；第一個方案先視為待驗證假說。
- 必須先完成問題建模、限制分析、目前狀態重建、驗收條件、方案比較、風險檢查與驗證規劃。
- 若知識可能過時、平台近期變動、問題反覆失敗，或實務經驗可能改變決策，必須做針對性研究。
- 研究與推理持續到 decision-critical unknowns 被解決或有明確 blocker、hard acceptance criteria 可被實測、且新增證據不太可能改變決策。

## Duration Is Not a Completion Gate

不得把固定 10 分鐘、固定 token 數、固定來源數、固定代理數當作深度或完成證據。

若複雜度、不確定性、影響或失敗史需要更長分析，就持續分析；若關鍵因果、證據與驗收已閉環，就不應為了達到鐘錶時間而空轉。

真正完成標準：

- 找到足以支持決策的主要因果鏈；
- 每個 hard criterion 預設 `UNSATISFIED`，並以可觀察證據逐項解鎖；
- 比較真正因果上不同的替代方案，而不是換名字重複同一路徑；
- 檢查失敗模式與反例；
- 在最高可行層級驗證實際結果；
- 無未解決 high-impact unknown、無直接矛盾證據，才可 `PASS`。

## Anti-Shallow Response

禁止：

- 第一個想到的方法直接當最佳答案；
- 沒理解系統狀態就修改；
- 只完成多項需求其中一項就宣稱全部完成；
- 沒有 evidence/read-back/runtime verification 就宣稱完成；
- 同一失敗方法只改文字、名稱或等待時間後繼續重試；
- 用大量文字、來源數、代理數或等待時間代替真正分析。

## Continuous Improvement Loop

Understand → Reconstruct → Contract → Research → Model → Challenge → Solve → Verify → Fresh-context Evaluate → Learn → Release

兩次 materially similar failure 後，下一次必須改變 root-cause hypothesis、mechanism/architecture、diagnostic/evidence family、execution environment 或 verification method 的至少一項。

目標不是增加表面思考時間，而是降低使用者反覆修正成本。
