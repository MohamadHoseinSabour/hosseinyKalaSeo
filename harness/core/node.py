"""Machine and Node identification module for multi-system distributed execution."""

import datetime
import os
import platform
import socket
import sys
from typing import Dict, Any, List
from harness.core.config import get_node_id

class NodeInfo:
    """Represents a worker node / machine running the harness."""
    
    def __init__(self, node_id: str = None, capabilities: List[str] = None):
        self.node_id = node_id or get_node_id()
        self.hostname = socket.gethostname()
        self.username = os.environ.get("USERNAME") or os.environ.get("USER") or "unknown"
        self.os_system = platform.system()
        self.os_release = platform.release()
        self.python_version = platform.python_version()
        self.capabilities = capabilities or ["seo", "content", "catalog", "wordpress_api"]
        self.last_heartbeat = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "hostname": self.hostname,
            "username": self.username,
            "os": f"{self.os_system} {self.os_release}",
            "python_version": self.python_version,
            "capabilities": self.capabilities,
            "last_heartbeat": self.last_heartbeat,
        }
    
    @classmethod
    def current(cls) -> "NodeInfo":
        return cls()
