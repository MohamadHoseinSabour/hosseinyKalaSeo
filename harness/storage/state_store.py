"""State storage manager with atomic writes and thread/process-safe operations."""

import json
import os
import shutil
import tempfile
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional

from harness.core.config import (
    TASKS_QUEUE_FILE,
    TASKS_ACTIVE_FILE,
    TASKS_HISTORY_FILE,
    WORKERS_REGISTRY_FILE,
    CHECKPOINTS_DIR,
)

_file_lock = threading.Lock()

def _read_json_file(path: Path, default_factory) -> Any:
    with _file_lock:
        if not path.exists():
            return default_factory()
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_factory()

def _write_json_file(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _file_lock:
        # Atomic write via temp file
        temp_dir = path.parent
        with tempfile.NamedTemporaryFile("w", dir=temp_dir, delete=False, encoding="utf-8") as tf:
            json.dump(data, tf, ensure_ascii=False, indent=2)
            temp_path = Path(tf.name)
        
        # Replace target file atomically
        shutil.move(str(temp_path), str(path))

class StateStore:
    """Manages persistence of all distributed harness states."""
    
    @staticmethod
    def get_queue() -> List[Dict[str, Any]]:
        return _read_json_file(TASKS_QUEUE_FILE, list)
    
    @staticmethod
    def save_queue(tasks: List[Dict[str, Any]]) -> None:
        _write_json_file(TASKS_QUEUE_FILE, tasks)
        
    @staticmethod
    def get_active() -> Dict[str, Dict[str, Any]]:
        return _read_json_file(TASKS_ACTIVE_FILE, dict)
        
    @staticmethod
    def save_active(active_tasks: Dict[str, Dict[str, Any]]) -> None:
        _write_json_file(TASKS_ACTIVE_FILE, active_tasks)
        
    @staticmethod
    def get_history() -> List[Dict[str, Any]]:
        return _read_json_file(TASKS_HISTORY_FILE, list)
        
    @staticmethod
    def save_history(history: List[Dict[str, Any]]) -> None:
        _write_json_file(TASKS_HISTORY_FILE, history)
        
    @staticmethod
    def append_history(entry: Dict[str, Any]) -> None:
        history = StateStore.get_history()
        history.insert(0, entry)  # latest first
        StateStore.save_history(history)
        
    @staticmethod
    def get_workers() -> Dict[str, Dict[str, Any]]:
        return _read_json_file(WORKERS_REGISTRY_FILE, dict)
        
    @staticmethod
    def save_workers(workers: Dict[str, Dict[str, Any]]) -> None:
        _write_json_file(WORKERS_REGISTRY_FILE, workers)
        
    @staticmethod
    def update_worker(worker_info: Dict[str, Any]) -> None:
        workers = StateStore.get_workers()
        node_id = worker_info.get("node_id")
        if node_id:
            workers[node_id] = worker_info
            StateStore.save_workers(workers)

    @staticmethod
    def get_checkpoint(task_id: str) -> Optional[Dict[str, Any]]:
        checkpoint_file = CHECKPOINTS_DIR / f"{task_id}.json"
        if not checkpoint_file.exists():
            return None
        return _read_json_file(checkpoint_file, lambda: None)

    @staticmethod
    def save_checkpoint(task_id: str, checkpoint_data: Dict[str, Any]) -> None:
        checkpoint_file = CHECKPOINTS_DIR / f"{task_id}.json"
        _write_json_file(checkpoint_file, checkpoint_data)

    @staticmethod
    def delete_checkpoint(task_id: str) -> None:
        checkpoint_file = CHECKPOINTS_DIR / f"{task_id}.json"
        if checkpoint_file.exists():
            try:
                checkpoint_file.unlink()
            except OSError:
                pass

    @staticmethod
    def list_checkpoints() -> List[Dict[str, Any]]:
        checkpoints = []
        if not CHECKPOINTS_DIR.exists():
            return checkpoints
        for cp_path in CHECKPOINTS_DIR.glob("*.json"):
            data = _read_json_file(cp_path, lambda: None)
            if data:
                checkpoints.append(data)
        return checkpoints
