"""定义 Wiki 摄入、日志和检查结果的数据结构。"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class RawSource:
    """表示从 raw source Markdown 解析出的资料。"""

    path: Path
    title: str
    url: str
    research_topic: str
    summary: str


@dataclass
class IngestResult:
    """记录一次 Ingest 创建、更新和跳过的页面。"""

    created_pages: list[Path] = field(default_factory=list)
    updated_pages: list[Path] = field(default_factory=list)
    skipped_sources: list[Path] = field(default_factory=list)


@dataclass(frozen=True)
class LintIssue:
    """表示一个 Wiki 健康检查问题。"""

    message: str
    path: Path | None = None


@dataclass
class LintReport:
    """保存 Wiki 健康检查结果。"""

    issues: list[LintIssue] = field(default_factory=list)
