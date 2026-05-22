# 架构说明

## 模块职责

- `src/domain_researcher/research/source_candidate.py`：定义 Deep Research 找到的候选资料。
- `src/domain_researcher/research/deep_research_adapter.py`：把 Deep Research 的 todo item 结果转换为候选资料。
- `src/domain_researcher/wiki/paths.py`：统一管理 memory 目录下的文件路径。
- `src/domain_researcher/wiki/bootstrap.py`：初始化 raw、wiki、schema、purpose 和 log。
- `src/domain_researcher/wiki/raw_store.py`：把候选资料保存为 raw source Markdown。
- `src/domain_researcher/wiki/models.py`：定义 raw source、ingest result 和 lint report 等数据结构。
- `src/domain_researcher/wiki/ingest.py`：把已确认 raw source 摄入 Wiki。
- `src/domain_researcher/wiki/writer.py`：写入来源页、主题页、索引页、总览和日志。
- `src/domain_researcher/wiki/reader.py`：读取 overview、index 和匹配主题页，为 Query 提供上下文。
- `src/domain_researcher/wiki/lint.py`：检查 Wiki 基础健康状态。
- `src/domain_researcher/workflows/research_to_raw.py`：编排研究结果到 raw sources 的保存流程。
- `src/domain_researcher/workflows/ingest_raw_to_wiki.py`：编排已确认 raw sources 到 Wiki 的摄入流程。
- `tests/`：保存单元测试。

## 调用关系

研究到 raw sources：

```text
todo items
  -> deep_research_adapter.candidates_from_todo_items()
  -> raw_store.save_raw_source()
  -> data/memory/raw/sources/*.md
```

raw sources 到 Wiki：

```text
confirmed raw source paths
  -> workflows.ingest_raw_to_wiki.ingest_confirmed_raw_sources()
  -> wiki.ingest.ingest_raw_source()
  -> wiki.writer 写来源页、主题页、index、overview、log
```

Query：

```text
用户问题
  -> wiki.reader.read_wiki_context()
  -> overview.md + index.md + 匹配 topic 页面
```

Lint：

```text
memory root
  -> wiki.lint.lint_wiki()
  -> LintReport
```

## 关键设计决定

- Deep Research 不直接写 Wiki，只保存 raw sources，避免未经确认的资料进入长期知识库。
- Ingest 只处理用户明确传入的 raw source 路径，不自动扫描全部目录。
- 第一版使用确定性规则生成 Wiki 页面，先固化文件生命周期，后续再接 LLM。
- 所有长期知识都用 Markdown 文件保存，便于人工查看和 Git 管理。
- `external_references/` 只放参考项目，不承载主项目代码。
