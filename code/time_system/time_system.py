from typing import Iterable, Optional

class TimeSystem:
    def __init__(self, rewindable_objects: Iterable = ()):
        self.rewindable_objects = list(rewindable_objects)
        self.time_stopped = False
        self.rewinding = False
        self.selected_object: Optional[object] = None

    def set_objects(self, objs: Iterable) -> None:
        """Обновить список объектов (если LevelLoader добавляет позже)."""
        self.rewindable_objects = list(objs)

    def toggle_time_stop(self) -> None:
        self.time_stopped = not self.time_stopped
        for obj in self.rewindable_objects:
            # ожидается метод set_paused у объектов
            if hasattr(obj, "set_paused"):
                obj.set_paused(self.time_stopped)

    def start_rewind(self) -> None:
        if self.rewinding:
            return
        self.rewinding = True
        # при старте перемотки выключаем стоп времени
        self.time_stopped = False
        for obj in self.rewindable_objects:
            if hasattr(obj, "set_rewinding"):
                obj.set_rewinding(True)

    def stop_rewind(self) -> None:
        if not self.rewinding:
            return
        self.rewinding = False
        for obj in self.rewindable_objects:
            if hasattr(obj, "set_rewinding"):
                obj.set_rewinding(False)

    def select_object(self, obj: object) -> None:
        self.selected_object = obj

    def clear_selection(self) -> None:
        self.selected_object = None

    def update(self, delta_time: float) -> None:
        """
        Обновляет rewindable объекты.
        - Если время остановлено и не перематывается — объекты не обновляются.
        - Если перемотка — объекты сами берут из истории.
        - В обычном режиме — объекты обновляются и записывают историю.
        """
        if self.time_stopped and not self.rewinding:
            return

        for obj in self.rewindable_objects:
            # объекты должны реализовать update(delta_time)
            obj.update(delta_time)
