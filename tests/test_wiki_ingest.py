"""测试 raw source 摄入 Wiki 的最小生命周期。"""

import tempfile
import unittest
from pathlib import Path

try:
    import path_setup  # noqa: F401
except ModuleNotFoundError:
    from tests import path_setup  # noqa: F401
from domain_researcher.wiki.bootstrap import bootstrap_wiki
from domain_researcher.wiki.ingest import ingest_raw_source


class WikiIngestTest(unittest.TestCase):
    """验证 Ingest 会创建页面并维护索引和日志。"""

    def test_ingest_raw_source_creates_source_topic_index_and_log(self):
        """摄入 raw source 后应创建来源页、主题页，并更新 index 与 log。"""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "memory"
            bootstrap_wiki(root, purpose="测试知识库")
            raw_path = root / "raw" / "sources" / "source-test.md"
            raw_path.write_text(
                "---\n"
                "title: \"测试资料\"\n"
                "url: \"https://example.com\"\n"
                "research_topic: \"测试主题\"\n"
                "---\n\n"
                "# 测试资料\n\n"
                "## 摘要\n\n"
                "这是资料摘要。\n",
                encoding="utf-8",
            )

            result = ingest_raw_source(root, raw_path)

            self.assertTrue(result.created_pages)
            self.assertTrue((root / "wiki" / "sources").is_dir())
            self.assertIn(
                "测试资料",
                (root / "wiki" / "index.md").read_text(encoding="utf-8"),
            )
            self.assertIn("ingest", (root / "log.md").read_text(encoding="utf-8"))
