"""Central Harness engine coordinating distributed tasks, leases, and lifecycle."""

import datetime
from typing import Dict, Any, List, Optional, Tuple
from harness.core.config import get_node_id, DEFAULT_LEASE_MINUTES
from harness.core.node import NodeInfo
from harness.core.task import Task
from harness.core.session import SessionContext
from harness.storage.state_store import StateStore

class HarnessEngine:
    """Core controller for multi-system distributed execution."""
    
    def __init__(self, node_id: Optional[str] = None):
        self.node_id = node_id or get_node_id()
        self.register_heartbeat()

    def register_heartbeat(self) -> None:
        """Register or update current worker node in registry."""
        node = NodeInfo(node_id=self.node_id)
        StateStore.update_worker(node.to_dict())

    def add_task(self, task: Task) -> str:
        """Add a new task to the queue."""
        queue = StateStore.get_queue()
        # Check duplicate id
        for t in queue:
            if t["id"] == task.id:
                raise ValueError(f"Task with ID '{task.id}' already exists in queue.")
                
        queue.append(task.to_dict())
        StateStore.save_queue(queue)
        return task.id

    def list_queue(self, category: Optional[str] = None) -> List[Task]:
        """List pending tasks, sorted by priority score descending."""
        raw_queue = StateStore.get_queue()
        tasks = [Task.from_dict(d) for d in raw_queue if d.get("status") == "PENDING"]
        if category:
            tasks = [t for t in tasks if t.category == category]
        tasks.sort(key=lambda t: t.priority_score, reverse=True)
        return tasks

    def list_active(self) -> List[Task]:
        """List currently claimed/in-progress tasks across all machines."""
        raw_active = StateStore.get_active()
        return [Task.from_dict(d) for d in raw_active.values()]

    def list_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List completed/failed tasks from history."""
        history = StateStore.get_history()
        return history[:limit]

    def claim_task(self, task_id: str) -> Optional[SessionContext]:
        """Claim a specific pending task from the queue."""
        self.register_heartbeat()
        queue = StateStore.get_queue()
        target_idx = -1
        target_dict = None
        
        for i, t in enumerate(queue):
            if t["id"] == task_id:
                target_idx = i
                target_dict = t
                break
                
        if target_idx == -1 or not target_dict:
            # Check if it's already active or resumable
            active = StateStore.get_active()
            if task_id in active:
                return self.resume_task(task_id)
            return None

        # Remove from queue
        queue.pop(target_idx)
        StateStore.save_queue(queue)
        
        # Mark claimed
        task = Task.from_dict(target_dict)
        now = datetime.datetime.now(datetime.timezone.utc)
        expires = now + datetime.timedelta(minutes=DEFAULT_LEASE_MINUTES)
        task.status = "CLAIMED"
        task.claimed_by = self.node_id
        task.claimed_at = now.isoformat()
        task.lease_expires_at = expires.isoformat()
        task.updated_at = now.isoformat()
        
        active = StateStore.get_active()
        active[task.id] = task.to_dict()
        StateStore.save_active(active)
        
        return SessionContext(task=task, node_id=self.node_id)

    def claim_next_task(self, category: Optional[str] = None) -> Optional[SessionContext]:
        """Claim the highest priority pending task in queue."""
        pending = self.list_queue(category=category)
        if not pending:
            return None
        return self.claim_task(pending[0].id)

    def find_resumable_tasks(self) -> List[Task]:
        """
        Find tasks that can be resumed:
        1. Tasks claimed by current node.
        2. Tasks claimed by any node whose lease has expired (orphaned / crashed).
        3. Checkpointed tasks in interrupted state.
        """
        active = self.list_active()
        resumable = []
        for t in active:
            # If claimed by me
            if t.claimed_by == self.node_id:
                resumable.append(t)
            # Or if lease has expired on another machine
            elif t.is_lease_expired():
                resumable.append(t)
            # Or has status CHECKPOINTED / INTERRUPTED
            elif t.status in ["CHECKPOINTED", "PAUSED", "FAILED"]:
                resumable.append(t)
        return resumable

    def resume_task(self, task_id: str) -> Optional[SessionContext]:
        """
        Resume an interrupted or orphaned task on current node.
        Transfers lease and loads previous checkpoint.
        """
        self.register_heartbeat()
        active = StateStore.get_active()
        task_data = active.get(task_id)
        
        if not task_data:
            # Check if checkpoint exists without active entry
            cp = StateStore.get_checkpoint(task_id)
            if cp:
                task_data = {
                    "id": task_id,
                    "title": cp.get("task_title", "Resumed Task"),
                    "status": "CHECKPOINTED",
                    "current_step_index": cp.get("current_step_index", 0),
                    "steps": [],
                }
            else:
                return None

        task = Task.from_dict(task_data)
        now = datetime.datetime.now(datetime.timezone.utc)
        expires = now + datetime.timedelta(minutes=DEFAULT_LEASE_MINUTES)
        
        # Transfer claim to current node
        task.status = "IN_PROGRESS"
        task.claimed_by = self.node_id
        task.claimed_at = now.isoformat()
        task.lease_expires_at = expires.isoformat()
        task.updated_at = now.isoformat()
        
        active[task.id] = task.to_dict()
        StateStore.save_active(active)
        
        ctx = SessionContext(task=task, node_id=self.node_id)
        ctx.checkpoint(
            step_index=task.current_step_index,
            step_name=task.current_step_name,
            message=f"Resumed execution on machine '{self.node_id}'",
        )
        return ctx

    def release_task(self, task_id: str) -> bool:
        """Release active task back into pending queue."""
        active = StateStore.get_active()
        task_data = active.pop(task_id, None)
        if not task_data:
            return False
            
        StateStore.save_active(active)
        task = Task.from_dict(task_data)
        task.status = "PENDING"
        task.claimed_by = None
        task.claimed_at = None
        task.lease_expires_at = None
        task.current_step_index = 0
        StateStore.delete_checkpoint(task_id)
        
        queue = StateStore.get_queue()
        queue.insert(0, task.to_dict())
        StateStore.save_queue(queue)
        return True

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Comprehensive snapshot for dashboard display."""
        self.register_heartbeat()
        workers = StateStore.get_workers()
        queue = self.list_queue()
        active = self.list_active()
        resumable = self.find_resumable_tasks()
        history = self.list_history(limit=10)
        checkpoints = StateStore.list_checkpoints()
        
        return {
            "current_node": self.node_id,
            "total_workers": len(workers),
            "workers": list(workers.values()),
            "queue_count": len(queue),
            "next_queued_tasks": [t.to_dict() for t in queue[:5]],
            "active_count": len(active),
            "active_tasks": [t.to_dict() for t in active],
            "resumable_count": len(resumable),
            "resumable_tasks": [t.to_dict() for t in resumable],
            "completed_history_count": len(StateStore.get_history()),
            "recent_completed": history[:5],
            "checkpoints_count": len(checkpoints),
        }
