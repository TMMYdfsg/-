
# -*- coding: utf-8 -*-
from pathlib import Path
import json
import hashlib
from typing import Any, Dict

class StateStore:
    """State is a single dict saved as JSON (state.json) under app user dir.
    """
    def __init__(self, user_dir: str):
        self.dir = Path(user_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.dir / "state.json"
        self.backup_dir = self.dir / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        # cache loaded state to avoid repeated disk reads
        self._state: Dict[str, Any] | None = None

    def load(self) -> Dict[str, Any]:
        if self._state is None:
            if self.state_path.exists():
                self._state = json.loads(
                    self.state_path.read_text(encoding="utf-8")
                )
            else:
                self._state = {}
        return self._state

    def save(self, st: Dict[str, Any]):
        self._state = st
        tmp = self.dir / "state.tmp"
        tmp.write_text(
            json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        tmp.replace(self.state_path)

    # Convenience wrappers used throughout the project
    def get_state(self) -> Dict[str, Any]:
        """Return current state, loading from disk if necessary."""
        return self.load()

    def update_state(self, st: Dict[str, Any]):
        """Persist given state to disk."""
        self.save(st)

    def backup(self) -> str:
        if not self.state_path.exists():
            return ""
        data = self.state_path.read_bytes()
        digest = hashlib.sha1(data).hexdigest()[:8]
        out = self.backup_dir / f"state_{digest}.json"
        out.write_bytes(data)
        return str(out)

    def reset(self):
        if self.state_path.exists():
            self.state_path.unlink()
