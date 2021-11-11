import argparse
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


def parse_book_page(response):
    comments_text = []
    genres = []

    soup = BeautifulSoup(response.text, "lxml")

    heading, author = soup.find("h1").text.split("::")

    image = soup.find("div", class_="bookimage").find("img")["src"]

    comments_text = [
        comment.find("span").text
        for comment in soup.find_all("div", class_="texts")
    ]

    genres = [
        book_genre.text
        for book_genre_tag in soup.find_all("span", class_="d_book")
        for book_genre in book_genre_tag.find_all("a")
    ]

    book_attributes = {
        "heading": heading.strip(),
        "author": author.strip(),
        "image": image,
        "comments": comments_text,
        "genres": genres,
    }

    return book_attributes


def check_for_redirect(response, url):
    if response.history and response.url != url:
        raise requests.HTTPError()


def download_txt(response, filename, folder="books/"):
    file_path = os.path.join(folder, sanitize_filename(filename))
    with open(file_path, "w") as file:
        file.write(response.text)

    return file_path


def download_image(response, filename, folder="images/"):
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path


def main():
    books_folder_name = "books/"
    images_folder_name = "images/"

    parser = argparse.ArgumentParser(
        description="Парсинг библиотеки tululu.ru"
    )
    parser.add_argument(
        "start_id", default=1, type=int, help="с какой страницы качать"
    )
    parser.add_argument(
        "end_id", default=10, type=int, help="по какую страницу качать"
    )
    args = parser.parse_args()

    os.makedirs(books_folder_name, exist_ok=True)
    os.makedirs(images_folder_name, exist_ok=True)

    for book_id in range(args.start_id, args.end_id + 1):
        payload = {"id": book_id}
        book_file_url = "https://tululu.org/txt.php"
        book_page_url = f"https://tululu.org/b{book_id}"
        try:
            book_file_response = requests.get(book_file_url, params=payload)
            book_file_response.raise_for_status()

            check_for_redirect(book_file_response, book_file_url)

            book_page_response = requests.get(book_page_url)
            book_page_response.raise_for_status()

            book_attributes = parse_book_page(book_page_response)
            heading = book_attributes["heading"]
            author = book_attributes["author"]
            image = book_attributes["image"]

            book_file_name = f"{book_id}. {heading}.txt"

            txt_file_path = download_txt(
                book_file_response, book_file_name, books_folder_name
            )

            image_url = urljoin(book_page_url, image)
            image_file_name = get_file_name(image_url)
            img_file_path = download_image(
                book_page_response, image_file_name, images_folder_name
            )
            print(f"Название: {heading}")
            print(f"Автор: {author}\n")
        except requests.exceptions.HTTPError:
            pass


if __name__ == "__main__":
    main()
