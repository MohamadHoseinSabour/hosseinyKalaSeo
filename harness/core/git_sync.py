"""Git synchronization helper for multi-machine harness state sharing."""

import subprocess
from pathlib import Path
from typing import Tuple
from harness.core.config import PROJECT_ROOT

class GitSync:
    """Provides git pull/push operations to keep multi-system state in sync."""
    
    @staticmethod
    def run_git(args: list[str]) -> Tuple[int, str, str]:
        try:
            res = subprocess.run(
                ["git"] + args,
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=45,
            )
            return res.returncode, res.stdout.strip(), res.stderr.strip()
        except Exception as e:
            return 1, "", str(e)

    @staticmethod
    def pull() -> Tuple[bool, str]:
        """Pull latest state changes from remote."""
        code, out, err = GitSync.run_git(["pull", "--rebase", "origin", "main"])
        if code == 0:
            return True, out or "Successfully updated from origin/main."
        return False, f"Git pull failed: {err or out}"

    @staticmethod
    def push_state(commit_msg: str = "chore(harness): update distributed state") -> Tuple[bool, str]:
        """Stage harness/state, commit, and push to origin."""
        # Stage state directory
        code, _, err = GitSync.run_git(["add", "harness/state/"])
        if code != 0:
            return False, f"Git add failed: {err}"
        
        # Check if there are changes to commit
        code, out, _ = GitSync.run_git(["status", "--porcelain", "harness/state/"])
        if not out:
            return True, "No state changes to commit."
            
        # Commit
        code, out, err = GitSync.run_git(["commit", "-m", commit_msg])
        if code != 0:
            return False, f"Git commit failed: {err or out}"
            
        # Push
        code, out, err = GitSync.run_git(["push", "origin", "main"])
        if code == 0:
            return True, "State successfully pushed to origin/main."
        return False, f"Git push failed: {err or out}"
