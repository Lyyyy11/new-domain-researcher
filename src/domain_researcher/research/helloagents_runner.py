"""接入 helloagents-deepresearch 的运行入口。"""

from pathlib import Path
from typing import Any
import sys


def run_helloagents_deep_research(topic: str, backend_src_path: Path | None = None) -> Any:
    """调用 helloagents-deepresearch 的 run_deep_research。"""
    if backend_src_path is not None:
        path_text = str(Path(backend_src_path))
        if path_text not in sys.path:
            sys.path.insert(0, path_text)

    try:
        from agent import run_deep_research
    except ImportError as exc:
        raise RuntimeError(
            "无法导入 helloagents-deepresearch，请传入 backend src 路径或先安装参考后端依赖。"
        ) from exc

    return run_deep_research(topic)
