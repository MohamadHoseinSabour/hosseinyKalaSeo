"""Hosseiny Kala Advanced Multi-System Distributed Harness System.

Provides distributed state coordination, task queueing, execution session
checkpointing, resume capability, rules & reminders enforcement, prompts registry,
and skill discovery for multi-node parallel execution.
"""

from harness.core.config import get_node_id, PROJECT_ROOT, HARNESS_DIR, STATE_DIR
from harness.core.node import NodeInfo
from harness.core.task import Task
from harness.core.session import SessionContext
from harness.core.engine import HarnessEngine
from harness.core.git_sync import GitSync
from harness.storage.state_store import StateStore
from harness.registry.skills_registry import SkillsRegistry, SkillInfo
from harness.registry.reminders_registry import RemindersRegistry, ReminderRule
from harness.registry.prompts_registry import PromptsRegistry, PromptTemplate

_engine_instance = None

def get_harness(node_id: str = None) -> HarnessEngine:
    """Singleton-like accessor to obtain HarnessEngine instance."""
    global _engine_instance
    if _engine_instance is None or (node_id and _engine_instance.node_id != node_id):
        _engine_instance = HarnessEngine(node_id=node_id)
    return _engine_instance

__all__ = [
    "get_harness",
    "get_node_id",
    "PROJECT_ROOT",
    "HARNESS_DIR",
    "STATE_DIR",
    "HarnessEngine",
    "Task",
    "SessionContext",
    "NodeInfo",
    "GitSync",
    "StateStore",
    "SkillsRegistry",
    "SkillInfo",
    "RemindersRegistry",
    "ReminderRule",
    "PromptsRegistry",
    "PromptTemplate",
]
