# Калькулятор на Python (Kivy)

Один код — приложение для ПК и мобильных устройств.

## Запуск на ПК (Windows / macOS / Linux)

```bash
pip install -r requirements.txt
python main.py
```

Управление: мышью, тачпадом или клавиатурой (цифры, `+ - * / %`, Enter, Backspace, Esc).

## Сборка под Android

На Linux (или WSL2 в Windows):

```bash
pip install buildozer
buildozer init          # создаст buildozer.spec
buildozer -v android debug
```

Готовый `.apk` появится в папке `bin/` — устанавливается на телефон как обычное приложение.

## iOS

Сборка под iOS выполняется на macOS через [kivy-ios](https://github.com/kivy/kivy-ios).

## Возможности

- Четыре арифметических действия, проценты, смена знака
- Большой адаптивный дисплей (шрифт уменьшается для длинных чисел)
- Поддержка клавиатуры на ПК
- Обработка ошибок (деление на ноль и т.п.)
