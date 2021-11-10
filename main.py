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


def parse_book(response):
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


def download_image(response, filename, folder="images/"):
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path


def main():
    books_amount = 10
    books_folder_name = "books/"
    books_dir = os.path.join(os.getcwd(), books_folder_name)
    os.makedirs(books_dir, exist_ok=True)

    images_folder_name = "images/"
    images_dir = os.path.join(os.getcwd(), images_folder_name)
    os.makedirs(images_dir, exist_ok=True)

    for book_id in range(1, books_amount + 1):
        book_file_url = f"https://tululu.org/txt.php?id={book_id}"
        try:
            book_file_response = requests.get(book_file_url)
            book_file_response.raise_for_status()

            check_for_redirect(book_file_response, book_file_url)

            book_page_url = f"https://tululu.org/b{book_id}"
            book_page_response = requests.get(book_page_url)
            book_page_response.raise_for_status()

            heading, author, img = parse_book(book_page_response)
            book_file_name = f"{book_id}. {heading.strip()}.txt"

            txt_file_path = download_txt(
                book_file_response, book_file_name, books_folder_name
            )

            image_url = urljoin(book_page_url, img)
            image_file_name = get_file_name(image_url)
            img_file_path = download_image(
                book_page_response, image_file_name, images_folder_name
            )
            # print(txt_file_path)
            print(img_file_path + " " + img)
        except requests.exceptions.HTTPError:
            pass


if __name__ == "__main__":
    main()
