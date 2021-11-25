import argparse
import json
import os

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse, unquote


def get_file_name(url):
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    _, file_name = os.path.split(path)

    return file_name


def check_for_redirect(response, url):
    if response.history and response.url != url:
        raise requests.HTTPError()


def parse_book_page(response):
    comments_text = []
    genres = []

    soup = BeautifulSoup(response.text, "lxml")

    heading, author = soup.select_one("h1").text.split("::")

    image = soup.select_one("div.bookimage img")["src"]

    comments_text = [comment.text for comment in soup.select("div.texts span")]

    genres = [book_genre.text for book_genre in soup.select("span.d_book a")]

    book_attributes = {
        "heading": heading.strip(),
        "author": author.strip(),
        "image": image,
        "comments": comments_text,
        "genres": genres,
    }

    return book_attributes


def download_txt(response, filename, folder="books/"):
    file_path = os.path.join(folder, sanitize_filename(filename))
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(response.text)

    return file_path


def download_image(response, filename, folder="images/"):
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path


def get_books_id(response):
    soup = BeautifulSoup(response.text, "lxml")

    books_id = [
        book_tags["href"]
        for book_tags in soup.select("table.d_book div.bookimage a")
    ]

    return books_id


def get_last_page_number(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    last_page_numbers = [
        page_number.text for page_number in soup.select("a.npage")
    ]

    return last_page_numbers[-1]


def main():
    fiction_books_attributes = []
    first_page_fiction_category_url = "http://tululu.org/l55/"

    parser = argparse.ArgumentParser(
        description="Парсинг библиотеки tululu.ru"
    )
    parser.add_argument(
        "--start_page",
        default=1,
        type=int,
        help="с какой страницы качать",
    )
    parser.add_argument(
        "--end_page",
        type=int,
        default=get_last_page_number(first_page_fiction_category_url),
        help="по какую страницу качать",
    )
    parser.add_argument(
        "--dest_folder",
        help="путь к каталогу с результатами парсинга: картинкам, книгам, JSON",
    )
    parser.add_argument(
        "--skip_imgs",
        action="store_true",
        help="не скачивать картинки",
    )
    parser.add_argument(
        "--skip_txt",
        action="store_true",
        help="не скачивать книги",
    )
    parser.add_argument(
        "--json_path",
        default="fiction_books.json",
        help="указать свой путь к *.json файлу с результатами",
    )
    args = parser.parse_args()

    personal_folder_name = args.dest_folder if args.dest_folder else ""
    books_folder_name = os.path.join(
        os.getcwd(), personal_folder_name, "books/"
    )
    images_folder_name = os.path.join(
        os.getcwd(), personal_folder_name, "images/"
    )

    if os.path.dirname(args.json_path):
        os.makedirs(os.path.dirname(args.json_path), exist_ok=True)

    for page in range(args.start_page, args.end_page + 1):
        fiction_category_url = f"http://tululu.org/l55/{page}/"
        response = requests.get(fiction_category_url)
        response.raise_for_status()
        books_id = get_books_id(response)
        for book_id in books_id:
            payload = {"id": book_id.replace("/", "").replace("b", "")}

            book_file_url = "https://tululu.org/txt.php"
            book_page_url = urljoin(fiction_category_url, book_id)

            try:
                book_file_response = requests.get(
                    book_file_url, params=payload
                )
                book_file_response.raise_for_status()

                check_for_redirect(book_file_response, book_file_url)

                book_page_response = requests.get(book_page_url)
                book_page_response.raise_for_status()

                book_attributes = parse_book_page(book_page_response)
                fiction_books_attributes.append(book_attributes)
                heading = book_attributes["heading"]
                image = book_attributes["image"]

                if not args.skip_txt:
                    os.makedirs(books_folder_name, exist_ok=True)
                    book_file_name = f"{book_id}. {heading}.txt"
                    txt_file_path = download_txt(
                        book_file_response, book_file_name, books_folder_name
                    )

                if not args.skip_imgs:
                    os.makedirs(images_folder_name, exist_ok=True)
                    image_url = urljoin(book_page_url, image)
                    image_file_name = get_file_name(image_url)
                    img_file_path = download_image(
                        book_page_response, image_file_name, images_folder_name
                    )
            except requests.exceptions.HTTPError:
                pass

    with open(args.json_path, "w") as json_file:
        json.dump(fiction_books_attributes, json_file, ensure_ascii=False)


if __name__ == "__main__":
    main()
