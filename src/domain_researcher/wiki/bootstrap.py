"""初始化 llm-wiki 风格的本地知识库目录。"""

from pathlib import Path

from domain_researcher.wiki.paths import WikiPaths


SCHEMA_TEXT = """# Wiki 维护规则

- raw sources 不直接修改。
- Wiki 页面必须记录 sources。
- 每次 ingest 必须更新 index 和 log。
- 页面之间使用 [[wikilink]]。
"""


def bootstrap_wiki(root: Path, purpose: str) -> WikiPaths:
    """创建 raw、wiki、schema、purpose 和 log 的基础结构。"""
    paths = WikiPaths(Path(root))

    for directory in (
        paths.raw_sources_dir,
        paths.research_runs_dir,
        paths.topics_dir,
        paths.entities_dir,
        paths.wiki_sources_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    _write_if_missing(paths.index_path, "# Wiki 索引\n\n暂无页面。\n")
    _write_if_missing(paths.overview_path, "# Wiki 总览\n\n暂无总览。\n")
    _write_if_missing(paths.log_path, "# 操作日志\n")
    _write_if_missing(paths.schema_path, SCHEMA_TEXT)
    _write_if_missing(paths.purpose_path, f"# 知识库目标\n\n{purpose}\n")

    return paths


def _write_if_missing(path: Path, text: str) -> None:
    """文件不存在时写入默认内容，避免覆盖已有 Wiki。"""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
