# -*- coding: utf-8 -*-
"""Кроссплатформенный калькулятор на Kivy.

Один и тот же код работает:
  - на ПК: Windows, macOS, Linux  ->  python main.py
  - на Android: сборка через Buildozer (см. README.md)
"""

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

Window.size = (360, 600)  # стартовый размер окна на ПК

BG_COLOR = get_color_from_hex("#1C1C1E")
BTN_COLOR = get_color_from_hex("#333333")
OP_COLOR = get_color_from_hex("#FF9F0A")
EQ_COLOR = get_color_from_hex("#34C759")
TEXT_COLOR = (1, 1, 1, 1)

BUTTONS = [
    ["C", "<-", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["+/-", "0", ".", "="],
]


class CalculatorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=8, **kwargs)

        self.expression = ""

        # Поле вывода
        self.display = Label(
            text="0",
            font_size="52sp",
            halign="right",
            valign="middle",
            size_hint_y=0.3,
            color=TEXT_COLOR,
        )
        self.display.bind(size=self._fit_text)
        self.add_widget(self.display)

        # Кнопки
        grid = GridLayout(cols=4, spacing=8, size_hint_y=0.7)
        for row in BUTTONS:
            for label in row:
                btn = Button(
                    text=label,
                    font_size="28sp",
                    background_normal="",
                    background_color=self._btn_color(label),
                    color=TEXT_COLOR,
                )
                btn.bind(on_release=self.on_button)
                grid.add_widget(btn)
        self.add_widget(grid)

        # Клавиатура (для ПК)
        Window.bind(on_key_down=self.on_key)

    @staticmethod
    def _btn_color(label):
        if label == "=":
            return EQ_COLOR
        if label in ("/", "*", "-", "+", "%"):
            return OP_COLOR
        return BTN_COLOR

    def _fit_text(self, *_):
        self.display.text_size = self.display.size
        # Уменьшаем шрифт, если число не влезает
        self.display.font_size = "52sp" if len(self.display.text) < 12 else "30sp"

    def on_button(self, btn):
        self.handle_input(btn.text)

    def on_key(self, _window, key, _scancode, _codepoint, modifiers, *_):
        keys = {
            273: "<-",        # backspace
            8: "<-",
            13: "=",          # enter
            271: "=",         # numpad enter
            27: "C",          # escape
        }
        if key in keys:
            self.handle_input(keys[key])
        else:
            ch = chr(key) if 32 <= key <= 126 else ""
            if ch in "0123456789.+-*/%":
                self.handle_input(ch)

    def handle_input(self, char):
        if char == "C":
            self.expression = ""
        elif char == "<-":
            self.expression = self.expression[:-1]
        elif char == "=":
            self.calculate()
        elif char == "+/-":
            self.negate()
        else:
            if char in "+-*/%" and (not self.expression or self.expression[-1] in "+-*/%"):
                # заменяем последний оператор, не допускаем оператор первым
                if not self.expression:
                    return
                self.expression = self.expression[:-1] + char
            else:
                self.expression += char

        self.display.text = self.expression or "0"

    def negate(self):
        if self.expression:
            try:
                value = -float(self.expression)
                self.expression = self._format(value)
            except ValueError:
                pass

    def calculate(self):
        try:
            expr = self.expression.replace("%", "/100")
            result = eval(expr, {"__builtins__": {}}, {})  # безопасный eval
            self.expression = self._format(result)
        except (ZeroDivisionError, SyntaxError, ValueError):
            self.expression = ""
            self.display.text = "Ошибка"
            return

    @staticmethod
    def _format(value):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return f"{value:.10g}"


class CalculatorApp(App):
    def build(self):
        self.title = "Калькулятор"
        Window.clearcolor = BG_COLOR
        return CalculatorLayout()


if __name__ == "__main__":
    CalculatorApp().run()
