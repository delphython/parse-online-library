# Парсим онлайн-библиотеку

Скрипт mail.py парсит онлайн библиотеку [БОЛЬШАЯ БЕСПЛАТНАЯ БИБЛИОТЕКА](https://tululu.org/). В результате скрипт скачает книги из раздела "Научная фантастика" в текстовом виде и картинки обложек в определенные папки, а также сформиhetn json файл с информацией по данным книгам.
Скрипт render_website.py формирует html страницы для развертывания своего личного [сайта - библиотеки](https://delphython.github.io/parse-online-library/).

## Предустановки

Python должен быть установлен. Используйте команду `pip` для установки зависимостей:
```bash
pip install -r requirements.txt
```

## Запуск скрипта для парсинга

Для запуска скрипта наберите в терминале команду:
```sh
python main.py --start_page --end_page --dest_folder --skip_imgs --skip_txt --json_path
```
Где аргумент '--start_page' - с какой страницы скачивать книги;

аргумент '--end_page' - по какую страницу скачивать книги - необязательный параметр. Если не указан, то скачаются все страницы, начиная с start_page;

аргумент '--dest_folder' - путь к каталогу с результатами парсинга: картинкам, книгам, JSON - необязательный параметр;

аргумент '--skip_imgs' - если указан, картинки скачиваться не будут - необязательный параметр;

аргумент '--skip_txt' - если указан, книги скачиваться не будут - необязательный параметр;

аргумент '--json_path' - указать свой путь к *.json файлу с результатами - необязательный параметр;

Например:
```sh
python main.py --start_page 20 --end_page 30 --dest_folder "fiction books" --skip_imgs --skip_txt --json_path "c:/test/books.json"
```
Для вывода справки наберите в теримнале команду:
```sh
python main.py -h
```
или
```sh
python main.py --help
```

## Запуск скрипта для ренлеринга

Для запуска скрипта наберите в терминале команду:
```sh
python render_website.py
```

## Meta

Vitaly Klyukin — [@delphython](https://t.me/delphython) — [delphython@gmail.com](mailto:delphython@gmail.com)

[https://github.com/delphython](https://github.com/delphython/)
