# 当前上下文

- 当前正在做什么：按新主计划 `docs/superpowers/plans/2026-05-23-deep-research-assisted-llm-wiki.md` 执行，已完成 Task 1 到 Task 4。
- 上次停在哪个位置：Task 4 已实现 raw source 保存能力，新增 `SourceCandidate` 和 `save_raw_source`。
- 近期关键决定和原因：当前目标已调整为 Deep Research-assisted LLM Wiki；Deep Research 只负责收集并保存 raw sources，避免未经确认的资料直接进入长期 Wiki。
- Wiki 方法决定：Wiki 创建、维护、Query、Lint 按 `llm-wiki.md` 的 Ingest / Query / Lint 方法实现；用户确认 raw sources 后才执行 Ingest。
- 参考项目边界：`helloagents-deepresearch` 只参考研究流程，`llm_wiki` 只参考长期 Wiki 方法；`external_references/` 只是参考项目目录，不写入主项目代码。
- 验收状态：Task 4 的 `tests.test_raw_source_store` 已通过，1 个测试通过、0 个失败。
- 下一步：继续执行 Task 5，从 Deep Research 结果提取 raw source candidates。
