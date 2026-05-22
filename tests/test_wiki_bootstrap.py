"""测试 Wiki 初始化是否创建 llm-wiki 风格目录。"""

import tempfile
import unittest
from pathlib import Path

try:
    import path_setup  # noqa: F401
except ModuleNotFoundError:
    from tests import path_setup  # noqa: F401
from domain_researcher.wiki.bootstrap import bootstrap_wiki


class WikiBootstrapTest(unittest.TestCase):
    """验证本地 Wiki 目录和基础文件能被初始化。"""

    def test_bootstrap_creates_llm_wiki_structure(self):
        """初始化后应创建 raw、wiki、schema、purpose 和 log。"""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "memory"

            bootstrap_wiki(root, purpose="研究某个主题")

            self.assertTrue((root / "raw" / "sources").is_dir())
            self.assertTrue((root / "raw" / "research_runs").is_dir())
            self.assertTrue((root / "wiki" / "index.md").is_file())
            self.assertTrue((root / "wiki" / "overview.md").is_file())
            self.assertTrue((root / "wiki" / "topics").is_dir())
            self.assertTrue((root / "wiki" / "entities").is_dir())
            self.assertTrue((root / "wiki" / "sources").is_dir())
            self.assertTrue((root / "log.md").is_file())
            self.assertTrue((root / "schema.md").is_file())
            self.assertTrue((root / "purpose.md").is_file())
