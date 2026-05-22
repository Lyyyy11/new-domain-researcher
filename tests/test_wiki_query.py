"""测试 Query 阶段能读取 Wiki 上下文。"""

import tempfile
import unittest
from pathlib import Path

try:
    import path_setup  # noqa: F401
except ModuleNotFoundError:
    from tests import path_setup  # noqa: F401
from domain_researcher.wiki.bootstrap import bootstrap_wiki
from domain_researcher.wiki.reader import read_wiki_context


class WikiQueryTest(unittest.TestCase):
    """验证 Wiki 查询上下文读取。"""

    def test_read_wiki_context_reads_index_overview_and_matching_topic(self):
        """应读取总览、索引和匹配主题页内容。"""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "memory"
            bootstrap_wiki(root, purpose="测试知识库")
            topic_path = root / "wiki" / "topics" / "燃气轮机.md"
            topic_path.write_text("# 燃气轮机\n\n已有结论。", encoding="utf-8")
            (root / "wiki" / "index.md").write_text(
                "- [[燃气轮机]]：主题页", encoding="utf-8"
            )
            (root / "wiki" / "overview.md").write_text("领域总览。", encoding="utf-8")

            context = read_wiki_context(root, "燃气轮机故障诊断")

            self.assertIn("领域总览", context)
            self.assertIn("已有结论", context)
