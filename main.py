import os

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def parse_book(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    title_tag = soup.find("h1")
    title_text = title_tag.text
    heading_author = title_text.split("::")

    if len(heading_author) == 1:
        heading_author.append("no author")

    return heading_author


def check_for_redirect(response, url):
    if response.history and response.url != url:
        raise requests.HTTPError()


def download_txt(url, filename, folder="books/"):
    response = requests.get(url)
    response.raise_for_status()

    file_path = os.path.join(folder, sanitize_filename(filename))

    try:
        check_for_redirect(response, url)
        with open(file_path, "wb") as file:
            file.write(response.content)

        return file_path
    except requests.exceptions.HTTPError:
        pass


def main():
    books_amount = 10
    books_folder_name = "books/"
    books_dir = os.path.join(os.getcwd(), books_folder_name)
    os.makedirs(books_dir, exist_ok=True)

    for book_id in range(1, books_amount + 1):
        book_file_url = f"https://tululu.org/txt.php?id={book_id}"
        book_url = f"https://tululu.org/b{book_id}"
        heading, author = parse_book(book_url)
        book_file_name = f"{book_id}. {heading.strip()}.txt"
        file_path = download_txt(
            book_file_url, book_file_name, books_folder_name
        )


if __name__ == "__main__":
    main()
