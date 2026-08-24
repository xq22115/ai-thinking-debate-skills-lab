# Continuous Reasoning Autonomous Loop v2

## Purpose
建立長流程任務處理機制，提升分析品質，而不是單純延長等待時間。

## Core Pipeline

1. Task Understanding
- 解析真正目標
- 建立需求與限制模型
- 定義驗收條件

2. Research Expansion
- 依任務複雜度收集高品質資料
- 優先官方文件、原始研究、GitHub、維護者討論與實務案例
- 避免低品質資料堆積

3. Deep Review Cycle
- 產生初步方案
- 主動尋找漏洞
- 比較替代方案
- 修正方案

4. Verification Gate
停止前確認：
- 是否真正解決目標
- 是否有未驗證假設
- 是否存在更佳方案
- 是否可能造成回歸問題

## Long Duration Thinking Policy

對大型研究、架構設計、除錯與高風險修改任務：

- 不採用立即輸出模式
- 必須完成分析循環後再輸出
- 以完成品質門檻作為結束條件

固定時間不是品質本身，核心是確保充分分析、驗證與修正。

## Self Improvement

每次任務完成後整理：

- 有效方法
- 失敗原因
- 可重用模式
- 未來判斷規則

目標：讓系統累積解題能力，而非每次重新開始。
