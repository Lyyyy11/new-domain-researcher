"""保存 Deep Research 找到的 raw sources。"""

import re
from pathlib import Path

from domain_researcher.research.source_candidate import SourceCandidate
from domain_researcher.wiki.paths import WikiPaths


def save_raw_source(root: Path, candidate: SourceCandidate) -> Path:
    """把候选资料保存成带元数据的 Markdown 文件。"""
    paths = WikiPaths(Path(root))
    paths.raw_sources_dir.mkdir(parents=True, exist_ok=True)

    source_id = _build_source_id(candidate)
    path = paths.raw_sources_dir / f"{source_id}.md"
    path.write_text(_render_raw_source(source_id, candidate), encoding="utf-8")
    return path


def _build_source_id(candidate: SourceCandidate) -> str:
    """根据时间和标题生成安全 source id。"""
    timestamp = candidate.retrieved_at[:19].replace("-", "").replace(":", "")
    timestamp = timestamp.replace("T", "-")
    return f"source-{timestamp}-{_slugify(candidate.title)}"


def _slugify(text: str) -> str:
    """把标题转换为适合文件名的简短 slug。"""
    slug = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "-", text).strip("-").lower()
    return slug or "untitled"


def _render_raw_source(source_id: str, candidate: SourceCandidate) -> str:
    """渲染 raw source 的 Markdown 内容。"""
    return (
        "---\n"
        f"id: {source_id}\n"
        f"title: \"{_escape(candidate.title)}\"\n"
        f"url: \"{_escape(candidate.url)}\"\n"
        f"source_type: \"{_escape(candidate.source_type)}\"\n"
        f"research_topic: \"{_escape(candidate.research_topic)}\"\n"
        f"retrieved_at: \"{_escape(candidate.retrieved_at)}\"\n"
        f"search_query: \"{_escape(candidate.search_query)}\"\n"
        f"task_title: \"{_escape(candidate.task_title)}\"\n"
        "status: \"pending_ingest\"\n"
        "---\n\n"
        f"# {candidate.title}\n\n"
        "## 摘要\n\n"
        f"{candidate.summary}\n\n"
        "## 原始片段\n\n"
        f"{candidate.raw_excerpt}\n\n"
        "## 来源说明\n\n"
        f"- URL: {candidate.url}\n"
        f"- 检索任务: {candidate.task_title}\n"
    )


def _escape(text: str) -> str:
    """转义 frontmatter 双引号。"""
    return text.replace('"', '\\"')
