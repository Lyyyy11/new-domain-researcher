"""测试 Deep Research 结果能转换为 raw source candidates。"""

import unittest
import tempfile
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

try:
    import path_setup  # noqa: F401
except ModuleNotFoundError:
    from tests import path_setup  # noqa: F401
from domain_researcher.research.deep_research_adapter import candidates_from_todo_items
from domain_researcher.research.helloagents_runner import run_helloagents_deep_research
from domain_researcher.workflows.research_to_raw import (
    run_deep_research_as_raw_sources,
    save_research_results_as_raw_sources,
)


@dataclass
class FakeResearchOutput:
    """模拟 helloagents-deepresearch 的 SummaryStateOutput。"""

    todo_items: list[dict[str, str]]


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

    def test_candidates_from_todo_items_extracts_helloagents_source_format(self):
        """应兼容 helloagents 后端实际输出的来源列表格式。"""
        todo_items = [
            {
                "title": "背景检索",
                "query": "测试主题 background",
                "summary": "任务总结",
                "sources_summary": "* 资料A : https://example.com/a\n* 资料B : https://example.com/b",
            }
        ]

        candidates = candidates_from_todo_items("测试主题", todo_items)

        self.assertEqual(len(candidates), 2)
        self.assertEqual(candidates[0].title, "资料A")
        self.assertEqual(candidates[0].url, "https://example.com/a")
        self.assertEqual(candidates[1].title, "资料B")
        self.assertEqual(candidates[1].url, "https://example.com/b")

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

    def test_run_deep_research_as_raw_sources_uses_real_api_shape(self):
        """真实 Deep Research 形状的输出应能直接保存为 raw sources。"""
        def fake_runner(topic: str) -> FakeResearchOutput:
            return FakeResearchOutput(
                todo_items=[
                    {
                        "title": "真实检索",
                        "query": f"{topic} research",
                        "summary": "真实任务总结",
                        "sources_summary": "- 标题: 真实资料\n  URL: https://example.com/real\n  摘要: 真实摘要",
                    }
                ]
            )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "memory"

            saved_paths = run_deep_research_as_raw_sources(root, "真实主题", fake_runner)

            self.assertEqual(len(saved_paths), 1)
            text = saved_paths[0].read_text(encoding="utf-8")
            self.assertIn("真实资料", text)
            self.assertIn("https://example.com/real", text)

    def test_run_helloagents_deep_research_uses_bundled_module(self):
        """runner 应优先调用主项目内置的 Deep Research 模块。"""
        with patch("importlib.import_module") as import_module:
            import_module.return_value.run_deep_research.return_value = "ok"

            result = run_helloagents_deep_research("测试主题")

            self.assertEqual(result, "ok")
            import_module.assert_called_once_with(
                "domain_researcher.research.deep_research.agent"
            )
