"""接入 helloagents-deepresearch 的运行入口。"""

from pathlib import Path
from typing import Any
import importlib


def run_helloagents_deep_research(topic: str, backend_src_path: Path | None = None) -> Any:
    """调用主项目内置的 helloagents Deep Research。"""
    if backend_src_path is not None:
        _ = backend_src_path
    try:
        module = importlib.import_module("domain_researcher.research.deep_research.agent")
    except ImportError as exc:
        raise RuntimeError(
            "无法导入内置 Deep Research，请先安装主项目依赖。"
        ) from exc

    return module.run_deep_research(topic)
