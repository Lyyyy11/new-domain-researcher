"""测试包，保存主项目的单元测试，并加载本地源码路径。"""

import sys
from pathlib import Path


# 让单元测试直接读取 src 下的主项目代码。
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
