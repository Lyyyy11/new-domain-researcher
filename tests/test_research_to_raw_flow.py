"""测试 Deep Research 结果能转换为 raw source candidates。"""

import unittest
import tempfile
from pathlib import Path

try:
    import path_setup  # noqa: F401
except ModuleNotFoundError:
    from tests import path_setup  # noqa: F401
from domain_researcher.research.deep_research_adapter import candidates_from_todo_items
from domain_researcher.workflows.research_to_raw import save_research_results_as_raw_sources


class ResearchToRawFlowTest(unittest.TestCase):
    """验证研究任务结果到候选资料的转换。"""

    def test_candidates_from_todo_items_extracts_sources(self):
        """应从任务来源摘要里提取标题、链接和研究主题。"""
        todo_items = [
            {
                "title": "背景检索",
                "query": "测试主题 background",
                "summary": "任务总结",
                "sources_summary": "- 标题: 资料A\n  URL: https://example.com/a\n  摘要: 资料摘要",
            }
        ]

        candidates = candidates_from_todo_items("测试主题", todo_items)

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].title, "资料A")
        self.assertEqual(candidates[0].url, "https://example.com/a")
        self.assertEqual(candidates[0].research_topic, "测试主题")

    def test_save_research_results_as_raw_sources_does_not_write_wiki(self):
        """研究工作流只保存 raw sources，不创建 Wiki 页面。"""
        todo_items = [
            {
                "title": "背景检索",
                "query": "测试主题 background",
                "summary": "任务总结",
                "sources_summary": "- 标题: 资料A\n  URL: https://example.com/a\n  摘要: 资料摘要",
            }
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "memory"

            paths = save_research_results_as_raw_sources(root, "测试主题", todo_items)

            self.assertEqual(len(paths), 1)
            self.assertTrue(paths[0].is_file())
            self.assertFalse((root / "wiki" / "topics").exists())
            self.assertFalse((root / "wiki" / "sources").exists())
