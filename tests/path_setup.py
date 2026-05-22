"""测试路径设置，让 unittest discover 能加载 src 下的项目代码。"""

import sys
from pathlib import Path


# discover 会把 tests 目录放入导入路径，这里再补上项目源码路径。
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
