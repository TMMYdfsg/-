# features/backup_manager.py
from __future__ import annotations
import json, time, os, glob
from pathlib import Path
from kivy.utils import platform

try:
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
except Exception:
    Permission = None

    def primary_external_storage_path() -> str:
        return str(Path.home())


from plyer import filechooser

APP_BACKUP_PREFIX = "shopgame_backup_"


def _ensure_storage_permissions():
    if platform == "android" and Permission:
        request_permissions(
            [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]
        )


def _default_backup_dir() -> Path:
    root = Path(primary_external_storage_path())
    return root / "Download" / "ShopGameBackups"


def export_backup(store, dest_dir: str | None = None) -> str:
    _ensure_storage_permissions()
    state = store.get_state()
    stamp = time.strftime("%Y%m%d_%H%M%S")
    fname = f"{APP_BACKUP_PREFIX}{stamp}.json"
    if dest_dir is None:
        chosen = filechooser.choose_dir(title="保存先フォルダを選択", multiple=False)
        dest_dir = chosen[0] if chosen else str(_default_backup_dir())
    out = Path(dest_dir) / fname
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(out)


def quick_export_backup(store) -> str:
    return export_backup(store, dest_dir=str(_default_backup_dir()))


def import_backup(store, path: str | None = None) -> str | None:
    _ensure_storage_permissions()
    if not path:
        picked = filechooser.open_file(
            title="バックアップjsonを選択", filters=[("JSON", "*.json")], multiple=False
        )
        if not picked:
            return None
        path = picked[0]
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "players" not in data:
        raise ValueError("不正なバックアップです（playersがありません）")
    store.update_state(data)
    return path


def list_backups() -> list[str]:
    _ensure_storage_permissions()
    pattern = str(_default_backup_dir() / f"{APP_BACKUP_PREFIX}*.json")
    files = glob.glob(pattern)
    files.sort(key=lambda p: Path(p).stat().st_mtime, reverse=True)
    return files


def import_latest_backup(store) -> str:
    files = list_backups()
    if not files:
        raise FileNotFoundError(
            "バックアップが見つかりません（Download/ShopGameBackups）"
        )
    return import_backup(store, files[0]) or ""
