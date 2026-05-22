"""读取 Wiki 内容，为 Query 阶段提供上下文。"""

from pathlib import Path

from domain_researcher.wiki.paths import WikiPaths


def read_wiki_context(root: Path, query: str, max_topics: int = 3) -> str:
    """读取 overview、index 和最多三个匹配主题页。"""
    paths = WikiPaths(Path(root))
    sections = [
        _read_if_exists(paths.overview_path),
        _read_if_exists(paths.index_path),
    ]

    for topic_path in _matching_topic_paths(paths.topics_dir, query)[:max_topics]:
        sections.append(topic_path.read_text(encoding="utf-8"))

    return "\n\n---\n\n".join(section for section in sections if section.strip())


def _matching_topic_paths(topics_dir: Path, query: str) -> list[Path]:
    """按查询词匹配主题页文件名或正文。"""
    if not topics_dir.exists():
        return []

    matched: list[Path] = []
    for path in sorted(topics_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if path.stem in query or any(char in text for char in query):
            matched.append(path)
    return matched


def _read_if_exists(path: Path) -> str:
    """文件存在时读取文本，否则返回空文本。"""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")
