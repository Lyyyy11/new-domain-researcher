"""把已确认的 raw source 摄入 llm-wiki 风格知识库。"""

from pathlib import Path

from domain_researcher.wiki.models import IngestResult, RawSource
from domain_researcher.wiki.paths import WikiPaths
from domain_researcher.wiki.writer import (
    append_log,
    update_index,
    update_overview,
    write_source_page,
    write_topic_page,
)


def ingest_raw_source(root: Path, raw_path: Path) -> IngestResult:
    """摄入单个 raw source，生成来源页和主题页。"""
    paths = WikiPaths(Path(root))
    source = _read_raw_source(Path(raw_path))
    result = IngestResult()

    source_page = write_source_page(paths, source)
    topic_page = write_topic_page(paths, source, source_page)
    result.created_pages.extend([source_page, topic_page])

    update_index(paths, source)
    update_overview(paths, source)
    append_log(paths, source.research_topic, result)
    return result


def _read_raw_source(raw_path: Path) -> RawSource:
    """从 raw source Markdown 中解析必要字段。"""
    text = raw_path.read_text(encoding="utf-8")
    frontmatter = _parse_frontmatter(text)
    return RawSource(
        path=raw_path,
        title=frontmatter.get("title", raw_path.stem),
        url=frontmatter.get("url", ""),
        research_topic=frontmatter.get("research_topic", "未分类主题"),
        summary=_extract_summary(text),
    )


def _parse_frontmatter(text: str) -> dict[str, str]:
    """解析简单 key: value frontmatter。"""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}

    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def _extract_summary(text: str) -> str:
    """提取摘要段落，找不到时返回空文本。"""
    marker = "## 摘要"
    if marker not in text:
        return ""
    after_marker = text.split(marker, 1)[1].strip()
    return after_marker.split("\n## ", 1)[0].strip()
