# Memory 文件格式

## 目录结构

```text
data/memory/
  raw/
    sources/
    research_runs/
  wiki/
    index.md
    overview.md
    topics/
    entities/
    sources/
  log.md
  schema.md
  purpose.md
```

## raw source

raw source 是 Deep Research 找到的原始资料记录。它默认不直接修改，状态初始为 `pending_ingest`。

示例：

```markdown
---
id: source-20260523-101500-test-title
title: "资料标题"
url: "https://example.com/article"
source_type: "web"
research_topic: "研究主题"
retrieved_at: "2026-05-23T10:15:00+08:00"
search_query: "实际检索词"
task_title: "Deep Research 子任务标题"
status: "pending_ingest"
---

# 资料标题

## 摘要

资料摘要。

## 原始片段

关键原始片段。

## 来源说明

- URL: https://example.com/article
- 检索任务: Deep Research 子任务标题
```

## Wiki source page

来源页说明某个 raw source 对 Wiki 的贡献。

```markdown
---
type: source
title: "资料标题"
source_id: "source-20260523-101500-test-title"
url: "https://example.com/article"
created_at: "2026-05-23T10:20:00+08:00"
sources:
  - "../../raw/sources/source-20260523-101500-test-title.md"
---

# 资料标题

## 核心贡献

这份资料提供的主要信息。

## 可关联主题

- [[研究主题]]
```

## Wiki topic page

主题页沉淀跨资料的长期认识。

```markdown
---
type: topic
title: "研究主题"
created_at: "2026-05-23T10:20:00+08:00"
updated_at: "2026-05-23T10:20:00+08:00"
sources:
  - "../sources/source-20260523-101500-test-title.md"
---

# 研究主题

## 当前认识

基于已摄入资料形成的稳定认识。

## 关键事实

- 事实。

## 争议和不确定点

- 暂无。

## 相关页面

- [[资料标题]]
```

## index.md

`index.md` 是 Wiki 导航入口，记录主题页和来源页。

## overview.md

`overview.md` 是当前知识库总览，给 Query 提供快速背景。

## log.md

`log.md` 是追加式操作记录。

```markdown
## [2026-05-23 10:10] ingest | 研究主题

- raw sources: 1
- created pages: 2
- updated pages: 0
- skipped sources: 0
```

## schema.md

`schema.md` 记录维护规则，包括 raw sources 不直接修改、Wiki 页面必须记录 sources、每次 ingest 必须更新 index 和 log、页面之间使用 `[[wikilink]]`。

## purpose.md

`purpose.md` 记录当前知识库目标和研究边界。
