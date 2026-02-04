from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from code.settings import BASE_DIR


CONFIG_PATH = BASE_DIR / "user_settings.json"


@dataclass
class AppConfig:
    width: int = 1280
    height: int = 720
    fullscreen: bool = False
    last_level: str = ""

    @classmethod
    def load(cls) -> "AppConfig":
        if not CONFIG_PATH.exists():
            return cls()
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            return cls(
                width=int(data.get("width", cls.width)),
                height=int(data.get("height", cls.height)),
                fullscreen=bool(data.get("fullscreen", cls.fullscreen)),
                last_level=str(data.get("last_level", "")),
            )
        except Exception:
            # Если файл битый — используем дефолт
            return cls()

    def save(self) -> None:
        payload = {
            "width": int(self.width),
            "height": int(self.height),
            "fullscreen": bool(self.fullscreen),
            "last_level": str(self.last_level or ""),
        }
        CONFIG_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def apply_window_config(window, cfg: AppConfig) -> None:
    """
    Применяет настройки окна.
    В arcade порядок такой: сначала fullscreen, потом set_size (иначе некоторые драйверы/ОС игнорируют).
    """
    # set_fullscreen есть в arcade.Window
    window.set_fullscreen(cfg.fullscreen)
    if not cfg.fullscreen:
        window.set_size(cfg.width, cfg.height)
