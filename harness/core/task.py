"""Task definition and lifecycle models for distributed harness."""

import datetime
import uuid
from typing import Dict, Any, List, Optional

PRIORITY_LEVELS = {
    "CRITICAL": 100,
    "HIGH": 75,
    "MEDIUM": 50,
    "LOW": 25,
}

TASK_STATUSES = [
    "PENDING",
    "CLAIMED",
    "IN_PROGRESS",
    "CHECKPOINTED",
    "PAUSED",
    "COMPLETED",
    "FAILED",
]

class Task:
    """Represents a work unit in the distributed pipeline."""
    
    def __init__(
        self,
        task_id: Optional[str] = None,
        title: str = "",
        category: str = "general",
        priority: str = "MEDIUM",
        status: str = "PENDING",
        tags: Optional[List[str]] = None,
        required_skills: Optional[List[str]] = None,
        steps: Optional[List[Dict[str, Any]]] = None,
        current_step_index: int = 0,
        claimed_by: Optional[str] = None,
        claimed_at: Optional[str] = None,
        lease_expires_at: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        completed_at: Optional[str] = None,
        created_by: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        artifacts: Optional[List[str]] = None,
        last_error: Optional[str] = None,
    ):
        self.id = task_id or f"TASK-{uuid.uuid4().hex[:8].upper()}"
        self.title = title
        self.category = category
        self.priority = priority.upper() if priority.upper() in PRIORITY_LEVELS else "MEDIUM"
        self.status = status.upper() if status.upper() in TASK_STATUSES else "PENDING"
        self.tags = tags or []
        self.required_skills = required_skills or []
        self.steps = steps or []
        self.current_step_index = current_step_index
        self.claimed_by = claimed_by
        self.claimed_at = claimed_at
        self.lease_expires_at = lease_expires_at
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.created_at = created_at or now_iso
        self.updated_at = updated_at or now_iso
        self.completed_at = completed_at
        self.created_by = created_by or "system"
        self.metadata = metadata or {}
        self.artifacts = artifacts or []
        self.last_error = last_error

    @property
    def priority_score(self) -> int:
        return PRIORITY_LEVELS.get(self.priority, 50)

    @property
    def total_steps(self) -> int:
        return len(self.steps)

    @property
    def current_step_name(self) -> str:
        if 0 <= self.current_step_index < len(self.steps):
            step = self.steps[self.current_step_index]
            return step.get("name", f"Step {self.current_step_index + 1}")
        return "Complete" if self.current_step_index >= len(self.steps) else "Not Started"

    @property
    def progress_percentage(self) -> int:
        if not self.steps:
            return 100 if self.status == "COMPLETED" else 0
        if self.status == "COMPLETED":
            return 100
        return int((self.current_step_index / len(self.steps)) * 100)

    def is_lease_expired(self) -> bool:
        if not self.lease_expires_at:
            return True
        try:
            expires = datetime.datetime.fromisoformat(self.lease_expires_at)
            now = datetime.datetime.now(datetime.timezone.utc)
            return now > expires
        except Exception:
            return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "priority": self.priority,
            "status": self.status,
            "tags": self.tags,
            "required_skills": self.required_skills,
            "steps": self.steps,
            "current_step_index": self.current_step_index,
            "claimed_by": self.claimed_by,
            "claimed_at": self.claimed_at,
            "lease_expires_at": self.lease_expires_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed_at": self.completed_at,
            "created_by": self.created_by,
            "metadata": self.metadata,
            "artifacts": self.artifacts,
            "last_error": self.last_error,
            "progress_percent": self.progress_percentage,
            "current_step_name": self.current_step_name,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        return cls(
            task_id=data.get("id"),
            title=data.get("title", ""),
            category=data.get("category", "general"),
            priority=data.get("priority", "MEDIUM"),
            status=data.get("status", "PENDING"),
            tags=data.get("tags", []),
            required_skills=data.get("required_skills", []),
            steps=data.get("steps", []),
            current_step_index=data.get("current_step_index", 0),
            claimed_by=data.get("claimed_by"),
            claimed_at=data.get("claimed_at"),
            lease_expires_at=data.get("lease_expires_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            completed_at=data.get("completed_at"),
            created_by=data.get("created_by"),
            metadata=data.get("metadata", {}),
            artifacts=data.get("artifacts", []),
            last_error=data.get("last_error"),
        )
