"""统一管理本地 Wiki 目录和文件路径。"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WikiPaths:
    """保存一个 Wiki 根目录下的常用路径。"""

    root: Path

    @property
    def raw_dir(self) -> Path:
        """返回 raw sources 的根目录。"""
        return self.root / "raw"

    @property
    def raw_sources_dir(self) -> Path:
        """返回原始资料目录。"""
        return self.raw_dir / "sources"

    @property
    def research_runs_dir(self) -> Path:
        """返回研究运行记录目录。"""
        return self.raw_dir / "research_runs"

    @property
    def wiki_dir(self) -> Path:
        """返回 Wiki 页面根目录。"""
        return self.root / "wiki"

    @property
    def topics_dir(self) -> Path:
        """返回主题页目录。"""
        return self.wiki_dir / "topics"

    @property
    def entities_dir(self) -> Path:
        """返回实体页目录。"""
        return self.wiki_dir / "entities"

    @property
    def wiki_sources_dir(self) -> Path:
        """返回 Wiki 来源页目录。"""
        return self.wiki_dir / "sources"

    @property
    def index_path(self) -> Path:
        """返回 Wiki 索引文件路径。"""
        return self.wiki_dir / "index.md"

    @property
    def overview_path(self) -> Path:
        """返回 Wiki 总览文件路径。"""
        return self.wiki_dir / "overview.md"

    @property
    def log_path(self) -> Path:
        """返回操作日志文件路径。"""
        return self.root / "log.md"

    @property
    def schema_path(self) -> Path:
        """返回维护规则文件路径。"""
        return self.root / "schema.md"

    @property
    def purpose_path(self) -> Path:
        """返回知识库目标文件路径。"""
        return self.root / "purpose.md"
