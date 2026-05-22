"""检查 Wiki 基础健康状态。"""

from pathlib import Path

from domain_researcher.wiki.models import LintIssue, LintReport
from domain_researcher.wiki.paths import WikiPaths


def lint_wiki(root: Path) -> LintReport:
    """检查基础文件、孤立主题和来源页元数据。"""
    paths = WikiPaths(Path(root))
    report = LintReport()

    _check_required_files(paths, report)
    _check_orphan_topics(paths, report)
    _check_source_frontmatter(paths, report)
    return report


def _check_required_files(paths: WikiPaths, report: LintReport) -> None:
    """检查 log、schema 和 purpose 是否存在。"""
    for path in (paths.log_path, paths.schema_path, paths.purpose_path):
        if not path.exists():
            report.issues.append(LintIssue(message=f"缺少必要文件: {path.name}", path=path))


def _check_orphan_topics(paths: WikiPaths, report: LintReport) -> None:
    """检查 topic 页面是否出现在 index.md。"""
    index_text = paths.index_path.read_text(encoding="utf-8") if paths.index_path.exists() else ""
    if not paths.topics_dir.exists():
        return

    for topic_path in sorted(paths.topics_dir.glob("*.md")):
        topic_name = topic_path.stem
        if f"[[{topic_name}]]" not in index_text and topic_name not in index_text:
            report.issues.append(
                LintIssue(message=f"孤立主题未出现在 index.md: {topic_name}", path=topic_path)
            )


def _check_source_frontmatter(paths: WikiPaths, report: LintReport) -> None:
    """检查 source 页面是否包含 sources frontmatter。"""
    if not paths.wiki_sources_dir.exists():
        return

    for source_path in sorted(paths.wiki_sources_dir.glob("*.md")):
        text = source_path.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1] if text.startswith("---") and "---" in text[3:] else ""
        if "sources:" not in frontmatter:
            report.issues.append(
                LintIssue(message=f"来源页缺少 sources 元数据: {source_path.name}", path=source_path)
            )
