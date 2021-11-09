import os

import requests
from dotenv import load_dotenv


def get_file_name(url):
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    _, file_name = os.path.split(path)

    return file_name


def download_file(url, filename, file_dir, params=None):
    response = requests.get(url, params)
    response.raise_for_status()

    file_path = os.path.join(file_dir, filename)

    with open(file_path, "wb") as file:
        file.write(response.content)


def main():
    load_dotenv()

    # dvmn_api_key = os.environ[""]

    # file_url = "https://tululu.org/txt.php?id=32168"
    # file_name = "Peski_Marsa.txt"

    books_amount = 10
    books_dir_name = "books"
    books_dir = os.path.join(os.getcwd(), books_dir_name)
    os.makedirs(books_dir, exist_ok=True)

    for book_id in range(1, books_amount + 1):
        book_file_name = f"id{book_id}.txt"
        book_file_url = f"https://tululu.org/txt.php?id={book_id}"
        download_file(book_file_url, book_file_name, books_dir)


if __name__ == "__main__":
    main()
