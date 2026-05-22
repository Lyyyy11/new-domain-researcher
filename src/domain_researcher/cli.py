"""命令行入口，提供研究、确认和摄入操作。"""

from argparse import ArgumentParser
from pathlib import Path
from typing import Callable

from domain_researcher.wiki.bootstrap import bootstrap_wiki
from domain_researcher.wiki.models import IngestResult
from domain_researcher.workflows.ingest_raw_to_wiki import ingest_confirmed_raw_sources
from domain_researcher.workflows.research_to_raw import run_deep_research_as_raw_sources


def confirm_pending_sources_and_ingest(
    root: Path,
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> IngestResult:
    """列出待摄入资料，用户确认后再写入 Wiki。"""
    raw_sources = _pending_raw_sources(Path(root))
    if not raw_sources:
        output_func("没有待确认的 raw sources。")
        return IngestResult()

    output_func("待确认 raw sources：")
    for index, path in enumerate(raw_sources, start=1):
        output_func(f"{index}. {_read_title(path)}")

    choice = input_func("请输入要摄入的编号，多个编号用逗号分隔，输入 all 摄入全部，直接回车取消：").strip()
    selected = _select_sources(raw_sources, choice)
    if not selected:
        output_func("已取消摄入。")
        return IngestResult()

    bootstrap_wiki(Path(root), purpose="Deep Research-assisted LLM Wiki")
    result = ingest_confirmed_raw_sources(Path(root), selected)
    output_func(f"已摄入 {len(selected)} 个 raw source。")
    return result


def main() -> None:
    """解析命令行参数并执行对应操作。"""
    parser = ArgumentParser(description="Deep Research-assisted LLM Wiki")
    subparsers = parser.add_subparsers(dest="command", required=True)

    research_parser = subparsers.add_parser("research", help="运行 Deep Research 并保存 raw sources")
    research_parser.add_argument("topic")
    research_parser.add_argument("--memory-root", default="data/memory")
    research_parser.add_argument("--backend-src-path", default=None)

    confirm_parser = subparsers.add_parser("confirm", help="确认并摄入 raw sources")
    confirm_parser.add_argument("--memory-root", default="data/memory")

    args = parser.parse_args()
    if args.command == "research":
        backend_path = Path(args.backend_src_path) if args.backend_src_path else None
        saved = run_deep_research_as_raw_sources(Path(args.memory_root), args.topic, backend_src_path=backend_path)
        print(f"已保存 {len(saved)} 个 raw source。")
    elif args.command == "confirm":
        confirm_pending_sources_and_ingest(Path(args.memory_root))


def _pending_raw_sources(root: Path) -> list[Path]:
    """返回待确认的 raw source 文件。"""
    sources_dir = root / "raw" / "sources"
    if not sources_dir.exists():
        return []
    pending = []
    for path in sorted(sources_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if 'status: "pending_ingest"' in text or "status: pending_ingest" in text:
            pending.append(path)
    return pending


def _select_sources(raw_sources: list[Path], choice: str) -> list[Path]:
    """根据用户输入选择 raw source。"""
    if not choice:
        return []
    if choice.lower() == "all":
        return raw_sources

    selected: list[Path] = []
    for part in choice.split(","):
        if not part.strip().isdigit():
            continue
        index = int(part.strip()) - 1
        if 0 <= index < len(raw_sources):
            selected.append(raw_sources[index])
    return selected


def _read_title(path: Path) -> str:
    """读取 raw source 的标题。"""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("title:"):
            return line.split(":", 1)[1].strip().strip('"')
    return path.stem


if __name__ == "__main__":
    main()
