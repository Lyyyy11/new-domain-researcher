"""编排 Deep Research 结果保存为 raw sources 的流程。"""

from pathlib import Path
from typing import Any, Iterable

from domain_researcher.research.deep_research_adapter import candidates_from_todo_items
from domain_researcher.wiki.raw_store import save_raw_source


def save_research_results_as_raw_sources(
    root: Path, research_topic: str, todo_items: Iterable[Any]
) -> list[Path]:
    """把研究任务结果转换并保存为 raw source 文件。"""
    saved_paths: list[Path] = []
    for candidate in candidates_from_todo_items(research_topic, todo_items):
        saved_paths.append(save_raw_source(root, candidate))
    return saved_paths
