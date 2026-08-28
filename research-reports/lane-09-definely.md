# Lane 09 Candidate — Definely Vault（REJECTED）

- **研究範圍**：僅 Definely 官方網域 `definely.com`。
- **最終裁定**：REJECTED / SUPERSEDED
- **工具／版本**：Definely Vault
- **原先誤判日期**：2026-08-13（撤銷）
- **官方來源**：https://www.definely.com/blogs/definely-launches-vault-ai-powered-knowledge-management-solution-for-legal-professionals

## 為什麼撤銷

初步研究曾把頁面可見的「August 13th」與 2026 當前脈絡結合，錯誤判定為 2026-08-13。後續 exact-head GitHub Actions artifact read-back 顯示該 seed page 的 machine-readable publication metadata 為 `2024-08-13`。再由 Definely 官方作者頁交叉查證，`Discover Definely Vault` 明確列為 `8.28.2024`。

因此 Vault 並不是 2026 年 6–8 月新發布工具，不能保留在主任務的 10 項 accepted catalog 中。

## 仍然成立、但不影響淘汰的事實

Vault 確實是 legal knowledge／precedent 工具，可在 Microsoft Word 中找出並插入 clauses/definitions，也能協助 draft 使用既有機構語言；但**功能符合 ≠ 發布日期符合**。

## 根因分析

原始錯誤來自：

1. 官方文章正文只顯示「August 13th」，未在可見標題附近顯示年份；
2. 搜尋引擎近期重新 crawl，容易造成「最近發布」錯覺；
3. 初步 catalog 對正文日期與 metadata 沒有做 owning-runtime artifact read-back。

修正後規則：若 visible date 缺年份，而 machine-readable metadata／官方 archive 可提供年份，必須以可交叉驗證的原始年份裁決；不得用 crawl freshness 或當前年份補齊。

## 驗收

- 官方 URL：PASS
- 法律 drafting relevance：PASS
- 2026-06-01～2026-08-31 發布日期：**FAIL（實際 2024）**
- 最終主任務採納：**NO**

此 branch 保留作為 rejected evidence，不再算 active 10-agent set。
