# 当前上下文

- 当前正在做什么：验证并修复内置 Deep Research 的真实运行流程。
- 上次停在哪个位置：已修复 `DeepResearchAgent.run()` 未消费 `_execute_task()` 生成器的问题，现在同步运行会真正执行搜索和任务总结。
- 近期关键决定和原因：当前目标已调整为 Deep Research-assisted LLM Wiki；Deep Research 只负责收集并保存 raw sources，避免未经确认的资料直接进入长期 Wiki。
- Wiki 方法决定：Wiki 创建、维护、Query、Lint 按 `llm-wiki.md` 的 Ingest / Query / Lint 方法实现；用户确认 raw sources 后才执行 Ingest。
- 参考项目边界：`helloagents-deepresearch` 已从参考项目转为主项目内置 Deep Research 核心能力来源；`external_references/` 后续只保留历史参考，不再作为运行依赖。
- 验收状态：Deep Research 同步执行修复后总测试已通过，13 个测试通过、0 个失败。
- 下一步：可把确定性 Ingest 替换为 LLM 生成，或把命令行确认入口升级为更友好的界面。
