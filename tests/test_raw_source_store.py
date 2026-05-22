"""测试 Deep Research 候选资料能保存为可追溯 Markdown。"""

import tempfile
import unittest
from pathlib import Path

from domain_researcher.research.source_candidate import SourceCandidate
from domain_researcher.wiki.raw_store import save_raw_source


class RawSourceStoreTest(unittest.TestCase):
    """验证 raw source 文件保存格式。"""

    def test_save_raw_source_writes_traceable_markdown(self):
        """保存后文件应包含状态、标题、链接和原始片段。"""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "memory"
            candidate = SourceCandidate(
                title="测试资料",
                url="https://example.com",
                source_type="web",
                research_topic="测试主题",
                search_query="测试 查询",
                task_title="背景检索",
                summary="这是摘要",
                raw_excerpt="这是原始片段",
            )

            path = save_raw_source(root, candidate)

            text = path.read_text(encoding="utf-8")
            self.assertIn("status: \"pending_ingest\"", text)
            self.assertIn("测试资料", text)
            self.assertIn("https://example.com", text)
            self.assertIn("这是原始片段", text)
