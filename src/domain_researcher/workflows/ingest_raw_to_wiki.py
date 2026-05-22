"""编排已确认 raw sources 摄入 Wiki 的流程。"""

from pathlib import Path
from typing import Iterable

from domain_researcher.wiki.ingest import ingest_raw_source
from domain_researcher.wiki.models import IngestResult


def ingest_confirmed_raw_sources(root: Path, raw_source_paths: Iterable[Path]) -> IngestResult:
    """只摄入明确传入的 raw source 路径。"""
    combined = IngestResult()
    for raw_path in raw_source_paths:
        result = ingest_raw_source(root, Path(raw_path))
        combined.created_pages.extend(result.created_pages)
        combined.updated_pages.extend(result.updated_pages)
        combined.skipped_sources.extend(result.skipped_sources)
    return combined
