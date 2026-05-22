"""测试内置 Deep Research 同步运行流程。"""

import unittest

try:
    import path_setup  # noqa: F401
except ModuleNotFoundError:
    from tests import path_setup  # noqa: F401
from domain_researcher.research.deep_research.agent import DeepResearchAgent
from domain_researcher.research.deep_research.models import TodoItem


class FakePlanner:
    """模拟任务规划器。"""

    def plan_todo_list(self, _state):
        """返回一个待执行任务。"""
        return [
            TodoItem(
                id=1,
                title="测试任务",
                intent="验证同步执行",
                query="测试查询",
            )
        ]

    def create_fallback_task(self, _state):
        """返回兜底任务。"""
        return TodoItem(id=1, title="兜底任务", intent="兜底", query="兜底查询")


class FakeReporting:
    """模拟报告生成器。"""

    def generate_report(self, state):
        """根据任务总结生成报告。"""
        summaries = [task.summary for task in state.todo_items if task.summary]
        return "\n".join(summaries)


class DeepResearchAgentRunTest(unittest.TestCase):
    """验证同步 run 会真正执行每个任务。"""

    def test_run_consumes_task_execution_generator(self):
        """同步 run 应消费 _execute_task 返回的生成器。"""
        agent = object.__new__(DeepResearchAgent)
        agent.planner = FakePlanner()
        agent.reporting = FakeReporting()
        agent._drain_tool_events = lambda *_args, **_kwargs: []
        agent._persist_final_report = lambda *_args, **_kwargs: None

        def fake_execute_task(state, task, *, emit_stream):
            task.sources_summary = "* 资料A : https://example.com/a"
            task.summary = "任务已执行"
            task.status = "completed"
            yield {"type": "task_status", "status": "completed"}

        agent._execute_task = fake_execute_task

        output = DeepResearchAgent.run(agent, "测试主题")

        self.assertEqual(output.todo_items[0].summary, "任务已执行")
        self.assertIn("任务已执行", output.report_markdown)
