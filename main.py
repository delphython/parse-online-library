import os

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


def parse_book(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    title_tag = soup.find("h1")
    title_text = title_tag.text
    book_attributes = title_text.split("::")

    if len(book_attributes) == 1:
        book_attributes.append("no author")

    img = soup.find("div", class_="bookimage").find("img")["src"]
    book_attributes.append(img)

    return book_attributes


def check_for_redirect(response, url):
    if response.history and response.url != url:
        raise requests.HTTPError()


def download_txt(response, filename, folder="books/"):
    file_path = os.path.join(folder, sanitize_filename(filename))
    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path


def main():
    books_amount = 10
    books_folder_name = "books/"
    books_dir = os.path.join(os.getcwd(), books_folder_name)
    os.makedirs(books_dir, exist_ok=True)

    for book_id in range(1, books_amount + 1):
        book_file_url = f"https://tululu.org/txt.php?id={book_id}"
        try:
            book_file_response = requests.get(book_file_url)
            book_file_response.raise_for_status()

            check_for_redirect(book_file_response, book_file_url)

            book_url = f"https://tululu.org/b{book_id}"
            heading, author, img = parse_book(book_url)
            book_file_name = f"{book_id}. {heading.strip()}.txt"

            file_path = download_txt(
                book_file_response, book_file_name, books_folder_name
            )
            print(urljoin(book_url, img))
        except requests.exceptions.HTTPError:
            pass


if __name__ == "__main__":
    main()
