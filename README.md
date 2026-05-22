# new-domain-researcher

## 项目简介

这是一个 Deep Research-assisted LLM Wiki 原型。

它的目标是把“先找资料，再沉淀成长期知识库”拆成清楚的两步：

1. Deep Research 负责收集资料，并保存为 raw sources。
2. 用户确认资料后，系统再把 raw sources 摄入本地 Wiki。

这样可以避免搜索到的临时资料直接污染长期知识库。

## 技术架构

项目使用 Python 标准库实现，第一版不依赖数据库、向量库或桌面应用。

主要部分：

- `research`：内置 Deep Research 核心能力，并把任务结果整理成候选资料。
- `wiki`：负责初始化 Wiki、保存 raw sources、Ingest、Query 和 Lint。
- `workflows`：把单个能力串成完整流程。
- `tests`：使用 `unittest` 做单元测试。

数据默认按 llm-wiki 风格保存为 Markdown 文件：

- `raw sources` 保存原始资料记录。
- `wiki` 保存长期知识页面。
- `schema.md` 保存维护规则。
- `purpose.md` 保存知识库目标。
- `log.md` 保存追加式操作记录。

## 本地运行方法

创建虚拟环境：

```powershell
python -m venv .venv
```

安装项目依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

运行测试：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

运行真实 Deep Research 并保存 raw sources：

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe -m domain_researcher.cli research "研究主题"
```

真实搜索需要在项目根目录 `.env` 中配置搜索和模型，例如：

```env
SEARCH_API=tavily
TAVILY_API_KEY=你的_tavily_key
LLM_PROVIDER=ollama
LOCAL_LLM=llama3.2
```

确认待摄入资料并写入 Wiki：

```powershell
$env:PYTHONPATH='src'
.\.venv\Scripts\python.exe -m domain_researcher.cli confirm
```

## 部署方法

第一版是本地文件原型，不需要部署服务。

如果要同步到 GitHub：

```powershell
git push
```

## 测试方法

运行全部测试：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

当前测试覆盖：

- Wiki 初始化。
- raw source 保存。
- Deep Research 结果适配。
- 真实 Deep Research 输出到 raw sources 的工作流。
- raw sources 人工确认入口。
- Ingest。
- Query。
- Lint。
- 两个工作流边界。

## 搜索记录

已搜索 `skills.sh` 和 GitHub 相关方案，结论如下：

- GitHub 上已有多个 `llm-wiki` 方向项目，常见做法是把 raw sources 和长期 Wiki 分层，核心操作是 Ingest、Query、Lint。
- `NiharShrotri/llm-wiki` 采用本地 LLM 维护 Markdown Wiki 的思路，强调从原始文档逐步编译为结构化知识库。
- `Pratiyush/llm-wiki` 强调从会话历史生成可搜索、可导出的 Wiki，并使用 schema 指导 ingest 和 query。
- `nvk/llm-wiki` 强调 raw evidence、compiled knowledge 和输出产物分离，和本项目的边界一致。
- `nashsu/llm_wiki` 是完整桌面应用方向，本项目只参考其 Wiki 方法，不复制桌面应用。
- 搜索结论：第一版继续保持轻量，本地 Markdown + raw sources + Ingest / Query / Lint 即可。

参考链接：

- https://github.com/NiharShrotri/llm-wiki
- https://github.com/Pratiyush/llm-wiki
- https://github.com/nvk/llm-wiki
- https://github.com/nashsu/llm_wiki
- https://llm-wiki.net/

## 已完成功能

- 初始化 llm-wiki 风格目录。
- 保存 Deep Research raw sources。
- 从 Deep Research todo items 提取候选资料。
- 内置 Deep Research 后端核心代码，可直接通过主项目环境运行并保存 raw sources。
- 增加命令行确认入口，选择 raw sources 后再摄入 Wiki。
- 把已确认 raw source 摄入 Wiki。
- 读取 Wiki 上下文用于 Query。
- 检查 Wiki 基础健康状态。
- 打通研究到 raw sources、raw sources 到 Wiki 两个工作流。

## 待办事项

- 后续把确定性 Ingest 替换为 LLM 生成。
- 把命令行确认入口升级为更友好的界面。
