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
        if self.time_stopped:
            for obj in self.rewindable_objects:
                # ожидается метод set_paused у объектов
                if obj.is_selected:
                    obj.stop_rewind()
                    obj.start_pause()
                else:
                    obj.stop_pause()
        else: 
            for obj in self.rewindable_objects: 
                obj.stop_pause()

    def start_rewind(self) -> None:
        # Если сейчас выключено и мы пытаемся включить — проверяем, есть ли выбранный объект
        if not self.rewinding:
            selected_exists = any(getattr(o, "is_selected", False) for o in self.rewindable_objects)
            if not selected_exists:
                # Нечего перематывать — игнорируем нажатие
                return

        # Toggle флаг
        self.rewinding = not self.rewinding

        if self.rewinding:
            for obj in self.rewindable_objects:
                if getattr(obj, "is_selected", False):
                    obj.stop_pause()
                    obj.start_rewind()
                else:
                    obj.stop_rewind()
        else:
            for obj in self.rewindable_objects:
                obj.stop_rewind()

        
        print("Rewind toggled:", self.rewinding, "selected objects:", [getattr(o,'is_selected',False) for o in self.rewindable_objects])

    def update(self, delta_time: float) -> None:
        if self.time_stopped and not self.rewinding:
            return

        for obj in self.rewindable_objects:
            obj.update(delta_time)
