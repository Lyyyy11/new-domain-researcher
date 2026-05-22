"""测试 Deep Research 结果能转换为 raw source candidates。"""

import unittest

try:
    import path_setup  # noqa: F401
except ModuleNotFoundError:
    from tests import path_setup  # noqa: F401
from domain_researcher.research.deep_research_adapter import candidates_from_todo_items


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
