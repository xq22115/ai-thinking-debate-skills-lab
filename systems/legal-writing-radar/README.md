# Legal Writing Radar

這是一套 repository-native 的 **GitHub Actions + Python CLI + Skill**，用途有兩個：

1. 以 10 條互不重複的官方來源研究線，持續追蹤法律／高風險企業寫作 AI 的新版本、發布與功能變化；
2. 把高階美國商務律師、企業法務與大型國際工程往來信件的「內行邏輯」變成可驗證、可重複的寫作規則，而不是只模仿表面語氣。

它不是 GitHub Marketplace App，也不假稱 GitHub-hosted runner 能做到字面上的永不中斷。GitHub schedule 是 best-effort；真正需要常駐 polling 時，使用 `watch` 模式放在經授權的 always-on/self-hosted runtime。

## 目前驗證範圍

固定驗證窗：`2026-06-01` ～ `2026-08-31`。

種子 catalog 僅接受：

- 官方 vendor-controlled URL；
- 公開發布日期落在指定區間；
- 明確屬於 AI writing/drafting，或直接支撐法律／企業高風險起草；
- 10 個 lane 各自唯一，不重複 vendor/tool/official URL；
- 不從二手文章猜日期、版本、可用性或免費方案。

### 10 條獨立研究線

| Lane | 工具／版本 | 官方日期 | 專門能力 |
|---|---|---:|---|
| 01 | Harvey II | 2026-08-18 | matter/project context、memory、法律推理、機構模板繼承 |
| 02 | Next Generation CoCounsel Legal | 2026-06-22 | 權威來源 → 分析 → 帶引用 drafting、transactional redline |
| 03 | Lexis+ with Protégé for In-House Legal and Compliance | 2026-07-08 | in-house legal/compliance 專用 AI 工作流 |
| 04 | LegalOn Prompt Workflows | 2026-07-28 | 100+ attorney-built 法律 workflow、clause/redline/counterproposal |
| 05 | Luminance Luna Crescent | 2026-06-19 | contract-specific vertical legal model 與 agentic contract work |
| 06 | GC AI Easy Edit | 2026-07-30 | Word tracked-change drafting/redlining、new clause drafting |
| 07 | Wordsmith for Payments — Three Legal AI Agents | 2026-07-09 | payments 合約、規則、policy、notice、attestation drafting |
| 08 | goHeather Version 3 | 2026-08-25 | chat-native contract/legal-document drafting from scratch |
| 09 | Definely Vault | 2026-08-13 | Word 內 precedent/clause retrieval 與 rapid contract creation |
| 10 | Upgraded WRITER Playbooks | 2026-07-13 | enterprise research→draft→review→publish reusable writing pipeline |

完整官方 URL、release status、功能與 evidence note 在：

`evidence/verified-tools-2026-06-08.json`

延後／淘汰候選也保留原因，例如僅宣布 Q4 beta 或只在會議 preview 的產品不拿來湊 10 個。

## 為什麼不是「搜到關鍵字就算」

`legal_writing_radar.py` 的每條 lane 都有自己的：

- `tool_id`；
- 官方 host allowlist；
- seed URL；
- discovery URL；
- drafting/legal 專用關鍵字。

Scanner 只會在官方 domain 內跟進連結。日期只接受頁面明示的 machine-readable publication metadata，例如 `article:published_time`、`datePublished` 或 `<time datetime=...>`；沒有日期就是 `unknown`，不會從網址、搜尋排序或今天日期推測。

HTTP 403、timeout、反爬封鎖會被記成 evidence artifact 的失敗狀態，不會被轉換成「已驗證」。這很重要：**來源擋 scanner ≠ 來源不存在，也 ≠ 驗證成功。**

## GitHub 執行拓撲

`.github/workflows/legal-writing-radar.yml`：

- `unit-and-evidence`：先跑 Python compile、單元測試、10-source seed catalog 驗證；
- `lane-scan`：matrix `01..10`，`fail-fast: false`，每條研究線獨立掃描並上傳 JSON artifact；
- `adjudicate`：另開 job 下載 10 個 artifact，重新核對 lane/tool identity 與 seed catalog，不相信 scanner 自己說 PASS；
- `workflow_dispatch`：可手動重跑；
- `schedule`：每小時 `:17`、`:47` 兩次，避開整點尖峰。

### 為什麼沒有宣稱 GitHub schedule = 24/7 daemon

GitHub scheduled workflow 是 best-effort，可能因 runner/平台負載延遲；public repository 長期無活動也可能使 schedule 停用。因此這個專案把「持續監控」拆成兩層：

- **GitHub hosted：** 半小時級定期檢查、手動重跑、artifact 可稽核；
- **always-on/self-hosted：** CLI `watch` 常駐 polling。

這樣不會用一條 cron 假裝「24 小時絕不斷」。

## CLI

從 repo root 執行。

### 驗證固定 10-source catalog

```bash
python systems/legal-writing-radar/legal_writing_radar.py verify
```

成功輸出：

```json
{
  "status": "PASS",
  "accepted_count": 10,
  "errors": []
}
```

### 單獨執行一條研究線

```bash
python systems/legal-writing-radar/legal_writing_radar.py scan \
  --lane 07 \
  --output /tmp/lane-07.json
```

Artifact 會記錄：URL、HTTP/reachability、redirect final URL、官方 domain 驗證、title、explicit published date、關鍵字命中、content SHA256 與錯誤資訊。

### 裁決 10 條研究線

```bash
python systems/legal-writing-radar/legal_writing_radar.py adjudicate \
  --directory /path/to/ten-lane-artifacts
```

### Always-on watch

```bash
python systems/legal-writing-radar/legal_writing_radar.py watch \
  --interval 900 \
  --output-dir /var/lib/legal-writing-radar
```

`--interval` 最低 60 秒。這個模式本身不會替你建立伺服器或保證主機永遠在線；它是給已授權、實際常駐的 host / self-hosted runner / service manager 使用。

## 「頂尖律師式」不是堆法言法語

真正有辨識度的地方通常不是神祕片語，而是資訊與法律效果控制：

1. **決策先行**：先說 position / recommendation / ask，再說歷史。
2. **record anchor**：日期、文件、instruction、meeting minute、contract reference。
3. **authority anchor**：有 verified clause / law / precedent 才引用；沒有就留待驗證。
4. **commitment control**：分清 inquiry、proposal、present position、conditional willingness、instruction、final commitment。
5. **conditionality / reciprocity**：條件跟著 proposal，不藏在尾段。
6. **risk allocation**：下一個決策、成本、時間、approval 由誰承擔要清楚。
7. **escalation posture**：clarification、executive escalation、formal notice、dispute、settlement 不混成同一種口氣。
8. **explicit close**：一個 action、一個 owner、一個 deadline / next step。

這些才是「內行」訊號。

## 四種 correspondence mode

### `executive-counsel`

適合 CEO、GC、board、重要客戶或對手方高層。先 bottom line，後證據，最後 decision / deadline。

### `transactional`

適合 negotiation、term sheet、contract redline、counterproposal。強制標明 commitment state、conditions、reciprocity。

### `dispute-preservation`

適合爭議立場與 formal record。重點是 disputed proposition、chronology、verified basis、cure/response、procedural deadline，不靠情緒化威嚇。

### `international-project`

適合 EPC、基建、國際工程、FIDIC-style communication。強制保留：

`project reference → chronology → verified notice basis → cause → effect → entitlement → quantum → requested instruction → deadline → records`

它不會因為「發生事件」就直接推成「一定有 entitlement」。

## 對「暗語」的 fail-closed 規則

以下字樣預設不自動加：

- `without prejudice`
- `for settlement purposes only`
- `subject to contract`
- `attorney-client privileged`
- `attorney work product`
- `all rights reserved`

這些可能牽涉不同法域、特定溝通目的、既有律師關係、證據規則或合約 notice mechanics。只有使用者提供依據，或 governing law/contract 已被驗證後才啟用。Header 本身不會魔法般創造 privilege；一般化 reservation 也不能取代合約規定的 addressee、method、content、time bar。

## 產生 correspondence blueprint

輸入 JSON：

```json
{
  "objective": "取得對方在期限前確認變更指示",
  "audience": "Employer's Representative",
  "project_reference": "PROJECT-X / PACKAGE-03",
  "known_facts": [
    "Site Instruction SI-17 received 2026-08-24"
  ],
  "contract_anchors": [
    "Sub-Clause 1.3 — Communications"
  ],
  "cause": "新增施工要求",
  "effect": "可能影響工期與成本",
  "entitlement": "待依合約與適用法律確認",
  "quantum": "待同期紀錄與估價確認",
  "requested_action": "請書面確認指示及後續估價程序",
  "deadline": "2026-08-31"
}
```

執行：

```bash
python systems/legal-writing-radar/legal_writing_radar.py compose \
  --mode international-project \
  --input facts.json \
  --output blueprint.json
```

若沒有 contract/legal authority，輸出會保留：

`[VERIFY CONTRACT / LEGAL AUTHORITY]`

而不是自動生成一個看似專業的條號。

## 測試

```bash
python -m unittest discover \
  -s systems/legal-writing-radar/tests \
  -p 'test_*.py'
```

測試特別防：

- 少於／多於 10 個 accepted records；
- 重複 tool ID / URL；
- 日期超出 2026-06-01..2026-08-31；
- 非官方 host；
- 從沒有 publication metadata 的 HTML 猜日期；
- discovery 跑出官方 domain；
- 沒 authority 卻虛構 clause/law；
- `without prejudice` / privilege 類 label 被自動塞入；
- 國際工程 claim chain 被簡化掉。

## 相關 Skill

`skills/13-elite-us-legal-business-correspondence.md`

該 Skill 是最終寫作行為規格；`style_playbook.json` 是 machine-readable 的同一套機制描述。
