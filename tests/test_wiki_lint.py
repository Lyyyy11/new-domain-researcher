"""测试 Wiki Lint 能发现基础维护问题。"""

import tempfile
import unittest
from pathlib import Path

try:
    import path_setup  # noqa: F401
except ModuleNotFoundError:
    from tests import path_setup  # noqa: F401
from domain_researcher.wiki.bootstrap import bootstrap_wiki
from domain_researcher.wiki.lint import lint_wiki


class WikiLintTest(unittest.TestCase):
    """验证 Wiki 健康检查报告。"""

    def test_lint_reports_orphan_topic(self):
        """未被 index 引用的 topic 应被报告。"""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "memory"
            bootstrap_wiki(root, purpose="测试知识库")
            topic_path = root / "wiki" / "topics" / "孤立主题.md"
            topic_path.write_text("# 孤立主题\n\n没有被 index 引用。", encoding="utf-8")

            report = lint_wiki(root)

            self.assertTrue(report.issues)
            self.assertIn("孤立主题", report.issues[0].message)
