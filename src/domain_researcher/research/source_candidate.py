"""定义 Deep Research 产出的候选原始资料模型。"""

from dataclasses import dataclass, field
from datetime import datetime, timezone


def _now_iso() -> str:
    """返回带时区的当前时间文本。"""
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


@dataclass(frozen=True)
class SourceCandidate:
    """表示一条待确认摄入的研究资料。"""

    title: str
    url: str
    source_type: str
    research_topic: str
    search_query: str
    task_title: str
    summary: str
    raw_excerpt: str
    retrieved_at: str = field(default_factory=_now_iso)
