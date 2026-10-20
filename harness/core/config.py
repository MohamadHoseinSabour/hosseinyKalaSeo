"""Configuration and constants for Hosseiny Kala Harness System."""

import os
import platform
import socket
from pathlib import Path

# Resolve base directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
HARNESS_DIR = PROJECT_ROOT / "harness"
STATE_DIR = HARNESS_DIR / "state"
CHECKPOINTS_DIR = STATE_DIR / "checkpoints"
PROMPTS_DIR = HARNESS_DIR / "prompts"
TEMPLATES_DIR = HARNESS_DIR / "templates"
SKILLS_DIR = PROJECT_ROOT / ".agent" / "skills"
DATA_DIR = PROJECT_ROOT / "data"

# Ensure runtime directories exist
STATE_DIR.mkdir(parents=True, exist_ok=True)
CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# State files
TASKS_QUEUE_FILE = STATE_DIR / "tasks_queue.json"
TASKS_ACTIVE_FILE = STATE_DIR / "tasks_active.json"
TASKS_HISTORY_FILE = STATE_DIR / "tasks_history.json"
WORKERS_REGISTRY_FILE = STATE_DIR / "workers_registry.json"

# Lease and concurrency settings
DEFAULT_LEASE_MINUTES = 45
HEARTBEAT_INTERVAL_MINUTES = 5

def get_node_id() -> str:
    """Return a unique deterministic identifier for this machine/worker node."""
    env_node_id = os.environ.get("HARNESS_NODE_ID")
    if env_node_id:
        return env_node_id.strip()
    
    hostname = socket.gethostname() or "unknown-host"
    username = os.environ.get("USERNAME") or os.environ.get("USER") or "default-user"
    os_name = platform.system().lower()
    return f"{hostname}_{username}_{os_name}".replace(" ", "_")
