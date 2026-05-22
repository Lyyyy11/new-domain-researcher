# Deep Research-assisted LLM Wiki 设计说明

## 目标

当前项目方向调整为 Deep Research-assisted LLM Wiki。

第一版只做“资料到 Wiki”的底层闭环：

1. 用户输入研究主题。
2. Deep Research 规划并执行资料收集。
3. Deep Research 把找到的资料保存为 raw sources。
4. 用户确认哪些 raw sources 可以进入知识库。
5. Wiki Ingest 读取已确认的 raw sources。
6. 系统生成或更新 Wiki 页面，并维护 `index.md`、`overview.md` 和 `log.md`。
7. 后续 Query 和 Lint 都基于 Wiki 工作。

## 产品边界

Deep Research 是 raw sources 获取入口，只负责找资料、整理候选来源和保存原始资料记录。

Deep Research 不直接写长期 Wiki，也不直接修改已有 Wiki 页面。这样可以让资料收集和知识沉淀分开，避免未经确认的搜索结果进入长期知识库。

Wiki 创建和维护遵循 `llm-wiki.md` 的方法：

- raw sources 是事实来源，写入后默认不改动。
- Wiki 是长期知识层，由 Ingest 负责创建和更新。
- `schema.md` 说明 Wiki 的维护规则。
- `purpose.md` 说明当前知识库的目标和边界。
- `index.md` 是导航入口。
- `log.md` 记录每次操作。
- 页面之间使用 `[[wikilink]]` 建立关联。

## 第一版范围

第一版只实现本地 Markdown 文件能力，不做完整桌面应用。

包含：

- 保存 Deep Research 找到的 raw sources。
- 初始化 Wiki 目录结构。
- 用户确认后，把 raw sources 摄入 Wiki。
- 更新来源页、主题页、索引页和日志。
- Query 读取 Wiki 上下文。
- Lint 检查 Wiki 的基础健康状态。

暂不包含：

- 自动写论文、报告或文献综述。
- 知识图谱可视化。
- 向量数据库。
- Chrome 剪藏。
- 自动文件夹监听。
- 未经用户确认就自动摄入资料。

## 参考项目关系

### helloagents-deepresearch

`helloagents-deepresearch` 只作为 Deep Research 流程参考。

当前项目会吸收它的底层思想：

- 把研究主题拆成搜索任务。
- 收集搜索结果。
- 对每个任务做简短总结。
- 保存可追溯的研究过程。
- 输出进度事件。

但当前项目会新增明确边界：Deep Research 的输出是 raw source candidates，而不是最终 Wiki 页面。

### llm_wiki

`llm_wiki` 只作为长期 Wiki 方法参考。

当前项目会采用它的核心方法：

- 三层结构：raw sources、Wiki、维护规则。
- 三个操作：Ingest、Query、Lint。
- Markdown 页面作为本地知识库载体。
- frontmatter 记录页面类型、来源和时间。
- `index.md`、`overview.md`、`log.md` 共同维护长期可读性。

当前项目只吸收必要底层能力，不复制完整桌面应用，也不把核心代码写入 `external_references/`。

## 关键约定

- `external_references/` 只放参考项目。
- 主项目代码写在 `src/domain_researcher/`。
- Deep Research 结果默认只进入 `raw sources`。
- 只有用户确认的 raw sources 才能进入 Wiki Ingest。
- Wiki 的 Query 和 Lint 只读取 Wiki 层，不直接依赖 Deep Research 临时结果。
