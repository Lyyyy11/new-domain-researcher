"""测试 raw sources 的命令行确认入口。"""

import tempfile
import unittest
from pathlib import Path

try:
    import path_setup  # noqa: F401
except ModuleNotFoundError:
    from tests import path_setup  # noqa: F401
from domain_researcher.cli import confirm_pending_sources_and_ingest
from domain_researcher.research.source_candidate import SourceCandidate
from domain_researcher.wiki.bootstrap import bootstrap_wiki
from domain_researcher.wiki.raw_store import save_raw_source


class RawSourceConfirmationTest(unittest.TestCase):
    """验证用户确认后才把 raw sources 摄入 Wiki。"""

    def test_confirm_pending_sources_ingests_selected_source_only(self):
        """选择第一个资料时，只摄入该资料。"""
        messages: list[str] = []

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "memory"
            bootstrap_wiki(root, purpose="测试知识库")
            save_raw_source(
                root,
                SourceCandidate(
                    title="资料一",
                    url="https://example.com/one",
                    source_type="web",
                    research_topic="测试主题",
                    search_query="查询",
                    task_title="任务",
                    summary="摘要一",
                    raw_excerpt="片段一",
                ),
            )
            save_raw_source(
                root,
                SourceCandidate(
                    title="资料二",
                    url="https://example.com/two",
                    source_type="web",
                    research_topic="测试主题",
                    search_query="查询",
                    task_title="任务",
                    summary="摘要二",
                    raw_excerpt="片段二",
                ),
            )

            result = confirm_pending_sources_and_ingest(
                root,
                input_func=lambda _prompt: "1",
                output_func=messages.append,
            )

            index_text = (root / "wiki" / "index.md").read_text(encoding="utf-8")
            self.assertTrue(result.created_pages)
            self.assertIn("资料一", index_text)
            self.assertNotIn("资料二", index_text)
            self.assertTrue(any("资料一" in message for message in messages))

    def test_confirm_pending_sources_bootstraps_wiki_when_missing(self):
        """未初始化 Wiki 时，确认入口应先创建 Wiki 目录。"""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "memory"
            save_raw_source(
                root,
                SourceCandidate(
                    title="资料一",
                    url="https://example.com/one",
                    source_type="web",
                    research_topic="测试主题",
                    search_query="查询",
                    task_title="任务",
                    summary="摘要一",
                    raw_excerpt="片段一",
                ),
            )

            result = confirm_pending_sources_and_ingest(
                root,
                input_func=lambda _prompt: "all",
                output_func=lambda _message: None,
            )

            self.assertTrue(result.created_pages)
            self.assertTrue((root / "wiki" / "sources").is_dir())
            self.assertTrue((root / "wiki" / "index.md").is_file())
