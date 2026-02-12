# code/core/rules_view.py
from pathlib import Path
import arcade

from code.core.ui_widgets import Button, ButtonGroup
from code.settings import ASSETS_DIR  # предполагается, что у вас есть ASSETS_DIR
# Если ASSETS_DIR нет — замените на Path("assets")

class RulesView(arcade.View):
    """
    Экран с правилами. Читает rules.txt из assets.
    Поддерживает прокрутку колесом и клавишами Up/Down, Esc возвращает назад.
    """

    def __init__(self, back_view=None):
        super().__init__()
        self.back_view = back_view
        self.ui = ButtonGroup()
        self._layout_dirty = True

        # Параметры прокрутки
        self.scroll_y = 0.0
        self.scroll_speed = 40  # пикселей за шаг клавиши
        self.content_height = 0  # вычисляется после загрузки текста

        # Загружаем текст правил
        # Попробуем взять ASSETS_DIR из настроек, иначе папка "assets"
        try:
            assets_dir = ASSETS_DIR
        except Exception:
            assets_dir = Path("assets")

        rules_path = Path(assets_dir) / "rules.txt"
        if rules_path.exists():
            self.rules_text = rules_path.read_text(encoding="utf-8")
        else:
            self.rules_text = "Файл rules.txt не найден в папке assets."

    def _ensure_layout(self):
        if not self._layout_dirty:
            return
        self._layout_dirty = False

        self.ui = ButtonGroup()
        width, height = self.window.get_size()
        button_w = min(420, width * 0.5)
        button_h = 52
        gap = 14
        start_y = height * 0.12

        def go_back():
            if self.back_view:
                self.window.show_view(self.back_view)
            else:
                # если back_view не передан — вернёмся в главное меню
                from code.core.menu_view import MenuView
                self.window.show_view(MenuView())

        # Кнопка назад
        self.ui.add(Button("Назад", width * 3 / 4, start_y, button_w, button_h, go_back))

        # Рассчитаем высоту контента (приблизительно) для ограничения прокрутки.
        # Используем ту же ширину, что и текст при рисовании (padding слева/справа)
        padding = 60
        text_width = width - padding * 2
        # Оценка высоты: используем arcade.get_text_image или грубую оценку по строкам
        # Упростим: посчитаем количество строк при wrap, используя arcade.draw_text с multiline
        # Здесь просто грубая оценка: средняя высота строки ~20 px при font_size=16
        font_size = 16
        # Примерная строка: разделим текст на строки по '\n' и дополнительно учтём переносы
        approx_lines = 0
        for paragraph in self.rules_text.splitlines():
            if not paragraph:
                approx_lines += 1
                continue
            # оценка переносов
            chars_per_line = max(40, int(text_width / (font_size * 0.5)))
            approx_lines += max(1, (len(paragraph) // chars_per_line) + 1)
        self.content_height = approx_lines * (font_size + 6) + 40  # padding сверху/снизу

    def on_draw(self):
        # Собираем UI
        self._ensure_layout()

        # Рисуем фон в стиле меню: сначала очистка, затем заголовок и т.д.
        self.clear()
        width, height = self.window.get_size()

        # Фоновый цвет — можно подобрать как в MenuView (если у вас есть константы, используйте их)
        arcade.draw_lrbt_rectangle_filled(0, width, 0, height, arcade.color.DARK_SLATE_GRAY)

        # Заголовок
        arcade.draw_text("ПРАВИЛА", width / 2, height * 0.88,
                         arcade.color.WHITE, font_size=36, anchor_x="center")

        # Рисуем текст правил с переносом и прокруткой
        padding = 60
        text_x = padding
        text_y_start = height * 0.82  # верхняя точка для текста
        font_size = 16
        color = arcade.color.LIGHT_GRAY

        # Применяем scroll_y: чем больше scroll_y, тем ниже начинается текст
        # Ограничим scroll_y так, чтобы не прокрутить слишком далеко
        max_scroll = max(0, self.content_height - (text_y_start - 80))
        self.scroll_y = max(0, min(self.scroll_y, max_scroll))

        # draw_text поддерживает multiline и width
        arcade.draw_text(
            self.rules_text,
            text_x,
            text_y_start - self.scroll_y,
            color,
            font_size=font_size,
            width=width - padding * 2,
            align="left",
            anchor_x="left",
            anchor_y="top",
            multiline=True,
        )

        # Рисуем UI (кнопка Назад)
        self.ui.draw()

    # Прокрутка колесом мыши
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # scroll_y > 0 — вверх, < 0 — вниз
        self.scroll_y -= scroll_y * self.scroll_speed
        # Ограничение в _ensure_layout/on_draw

    # Клавиши вверх/вниз и Esc
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if self.back_view:
                self.window.show_view(self.back_view)
            else:
                from code.core.menu_view import MenuView
                self.window.show_view(MenuView())
            return
        if key == arcade.key.UP:
            self.scroll_y -= self.scroll_speed
        elif key == arcade.key.DOWN:
            self.scroll_y += self.scroll_speed
        elif key == arcade.key.PAGEUP:
            self.scroll_y -= self.scroll_speed * 6
        elif key == arcade.key.PAGEDOWN:
            self.scroll_y += self.scroll_speed * 6

    def on_mouse_motion(self, x, y, dx, dy):
        self._ensure_layout()
        self.ui.on_mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self._ensure_layout()
        self.ui.on_mouse_press(x, y, button)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self._layout_dirty = True
