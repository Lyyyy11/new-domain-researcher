"""把 Deep Research 任务结果转换为候选原始资料。"""

import re
from typing import Any, Iterable

from domain_researcher.research.source_candidate import SourceCandidate


def candidates_from_todo_items(
    research_topic: str, todo_items: Iterable[Any]
) -> list[SourceCandidate]:
    """从 Deep Research 的任务结果中提取资料候选项。"""
    candidates: list[SourceCandidate] = []
    for item in todo_items:
        task_title = _get_value(item, "title")
        search_query = _get_value(item, "query")
        task_summary = _get_value(item, "summary")
        sources_summary = _get_value(item, "sources_summary")

        for source in _parse_sources_summary(sources_summary):
            candidates.append(
                SourceCandidate(
                    title=source["title"],
                    url=source["url"],
                    source_type="web",
                    research_topic=research_topic,
                    search_query=search_query,
                    task_title=task_title,
                    summary=source.get("summary") or task_summary,
                    raw_excerpt=sources_summary,
                )
            )
    return candidates


def _get_value(item: Any, field_name: str) -> str:
    """兼容字典和对象两种任务结构。"""
    if isinstance(item, dict):
        return str(item.get(field_name, "") or "")
    return str(getattr(item, field_name, "") or "")


def _parse_sources_summary(text: str) -> list[dict[str, str]]:
    """从来源摘要文本中提取标题、URL 和摘要。"""
    if not text.strip():
        return []

    sources = []
    for match in _parse_labeled_sources(text):
        sources.append(
            {
                "title": match.group("title").strip(),
                "url": match.group("url").strip(),
                "summary": (match.group("summary") or "").strip(),
            }
        )
    if sources:
        return sources

    for match in _parse_bullet_sources(text):
        sources.append(
            {
                "title": match.group("title").strip(),
                "url": match.group("url").strip(),
                "summary": "",
            }
        )
    return sources


def _parse_labeled_sources(text: str):
    """解析“标题 / URL / 摘要”格式来源。"""
    return re.finditer(
        r"标题:\s*(?P<title>.+?)\s*\n\s*URL:\s*(?P<url>\S+)(?:\s*\n\s*摘要:\s*(?P<summary>.+))?",
        text,
    )


def _parse_bullet_sources(text: str):
    """解析 helloagents 实际输出的“* 标题 : URL”格式来源。"""
    return re.finditer(
        r"^\s*[*-]\s*(?P<title>.+?)\s*:\s*(?P<url>https?://\S+)\s*$",
        text,
        flags=re.MULTILINE,
    )
