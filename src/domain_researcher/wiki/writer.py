"""负责写入 Wiki 页面、索引、总览和日志。"""

from datetime import datetime, timezone
from pathlib import Path

from domain_researcher.wiki.models import IngestResult, RawSource
from domain_researcher.wiki.paths import WikiPaths


def write_source_page(paths: WikiPaths, source: RawSource) -> Path:
    """根据 raw source 创建 Wiki 来源页。"""
    page_path = paths.wiki_sources_dir / source.path.name
    content = (
        "---\n"
        "type: source\n"
        f"title: \"{_escape(source.title)}\"\n"
        f"source_id: \"{source.path.stem}\"\n"
        f"url: \"{_escape(source.url)}\"\n"
        f"created_at: \"{_now_iso()}\"\n"
        "sources:\n"
        f"  - \"../../raw/sources/{source.path.name}\"\n"
        "---\n\n"
        f"# {source.title}\n\n"
        "## 核心贡献\n\n"
        f"{source.summary}\n\n"
        "## 可关联主题\n\n"
        f"- [[{source.research_topic}]]\n"
    )
    page_path.write_text(content, encoding="utf-8")
    return page_path


def write_topic_page(paths: WikiPaths, source: RawSource, source_page: Path) -> Path:
    """根据研究主题创建或更新 Wiki 主题页。"""
    page_path = paths.topics_dir / f"{source.research_topic}.md"
    relative_source = f"../sources/{source_page.name}"
    if page_path.exists():
        text = page_path.read_text(encoding="utf-8")
        if relative_source not in text:
            text = text.rstrip() + f"\n- {relative_source}\n"
        page_path.write_text(text, encoding="utf-8")
        return page_path

    content = (
        "---\n"
        "type: topic\n"
        f"title: \"{_escape(source.research_topic)}\"\n"
        f"created_at: \"{_now_iso()}\"\n"
        f"updated_at: \"{_now_iso()}\"\n"
        "sources:\n"
        f"  - \"{relative_source}\"\n"
        "---\n\n"
        f"# {source.research_topic}\n\n"
        "## 当前认识\n\n"
        f"基于 [[{source.title}]] 形成初步认识。\n\n"
        "## 关键事实\n\n"
        f"- {source.summary}\n\n"
        "## 争议和不确定点\n\n"
        "- 暂无。\n\n"
        "## 相关页面\n\n"
        f"- [[{source.title}]]\n"
    )
    page_path.write_text(content, encoding="utf-8")
    return page_path


def update_index(paths: WikiPaths, source: RawSource) -> None:
    """更新 Wiki 索引入口。"""
    content = (
        "# Wiki 索引\n\n"
        "## 主题\n\n"
        f"- [[{source.research_topic}]]：主题页\n\n"
        "## 来源\n\n"
        f"- [[{source.title}]]：来源页\n"
    )
    paths.index_path.write_text(content, encoding="utf-8")


def update_overview(paths: WikiPaths, source: RawSource) -> None:
    """更新 Wiki 总览。"""
    content = (
        "# Wiki 总览\n\n"
        f"当前围绕“{source.research_topic}”沉淀知识。\n\n"
        f"最新摄入资料：[[{source.title}]]。\n"
    )
    paths.overview_path.write_text(content, encoding="utf-8")


def append_log(paths: WikiPaths, topic: str, result: IngestResult) -> None:
    """追加一次 Ingest 操作记录。"""
    timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"\n## [{timestamp}] ingest | {topic}\n\n"
        f"- raw sources: {len(result.created_pages) + len(result.updated_pages)}\n"
        f"- created pages: {len(result.created_pages)}\n"
        f"- updated pages: {len(result.updated_pages)}\n"
        f"- skipped sources: {len(result.skipped_sources)}\n"
    )
    with paths.log_path.open("a", encoding="utf-8") as file:
        file.write(entry)


def _now_iso() -> str:
    """返回当前时间。"""
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _escape(text: str) -> str:
    """转义 frontmatter 双引号。"""
    return text.replace('"', '\\"')
