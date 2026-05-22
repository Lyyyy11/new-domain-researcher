# 当前上下文

- 当前正在做什么：继续扩展第一版底层闭环，已完成 Task A 和 Task B。
- 上次停在哪个位置：已新增真实 `helloagents-deepresearch` 输出接入点，并新增命令行确认入口，可选择 pending raw sources 后再摄入 Wiki。
- 近期关键决定和原因：当前目标已调整为 Deep Research-assisted LLM Wiki；Deep Research 只负责收集并保存 raw sources，避免未经确认的资料直接进入长期 Wiki。
- Wiki 方法决定：Wiki 创建、维护、Query、Lint 按 `llm-wiki.md` 的 Ingest / Query / Lint 方法实现；用户确认 raw sources 后才执行 Ingest。
- 参考项目边界：`helloagents-deepresearch` 只参考研究流程，`llm_wiki` 只参考长期 Wiki 方法；`external_references/` 只是参考项目目录，不写入主项目代码。
- 验收状态：Task A 的 `tests.test_research_to_raw_flow` 已通过，3 个测试通过、0 个失败；Task B 的 `tests.test_raw_source_confirmation` 已通过，1 个测试通过、0 个失败。
- 下一步：可把确定性 Ingest 替换为 LLM 生成，或把命令行确认入口升级为更友好的界面。
