# 当前上下文

- 当前正在做什么：继续验证真实 Deep Research 到 raw sources 的流程。
- 上次停在哪个位置：已修复来源解析器，兼容 `helloagents-deepresearch` 实际输出的 `* 标题 : URL` 来源格式。
- 近期关键决定和原因：当前目标已调整为 Deep Research-assisted LLM Wiki；Deep Research 只负责收集并保存 raw sources，避免未经确认的资料直接进入长期 Wiki。
- Wiki 方法决定：Wiki 创建、维护、Query、Lint 按 `llm-wiki.md` 的 Ingest / Query / Lint 方法实现；用户确认 raw sources 后才执行 Ingest。
- 参考项目边界：`helloagents-deepresearch` 只参考研究流程，`llm_wiki` 只参考长期 Wiki 方法；`external_references/` 只是参考项目目录，不写入主项目代码。
- 验收状态：来源解析修复后总测试已通过，11 个测试通过、0 个失败。
- 下一步：可把确定性 Ingest 替换为 LLM 生成，或把命令行确认入口升级为更友好的界面。
