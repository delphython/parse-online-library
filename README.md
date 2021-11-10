# Парсим онлайн-библиотеку

Скрипт парсит онлайн библиотеку [БОЛЬШАЯ БЕСПЛАТНАЯ БИБЛИОТЕКА](https://tululu.org/). В результате скрипт выведет на экран название и автора книг и скачает книги в текстовом виде и картинки обложек в определенные папки.

## Предустановки

Python3 должен быть установлен. Используйте команду `pip` для установки зависимостей:
```bash
pip install -r requirements.txt
```

## Запуск скрипта

Для запуска скрипта наберите в теримнале команду:
```sh
python main.py --start_id --end_id
```
Где аргумент '--start_id' - с какой страницы скачивать книги;
аргумент '--end_id' - по какую страницу скачивать книги.
Например:
```sh
python main.py 10 20
```
Для вывода справки наберите в теримнале команду:
```sh
python main.py -h
```
или
```sh
python main.py --help
```

## Meta

Vitaly Klyukin — [@delphython](https://t.me/delphython) — [delphython@gmail.com](mailto:delphython@gmail.com)

[https://github.com/delphython](https://github.com/delphython/)
