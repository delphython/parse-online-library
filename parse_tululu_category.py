import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote


def get_books_id(response):
    soup = BeautifulSoup(response.text, "lxml")

    books_id = [
        book_tags["href"]
        for table_tags in soup.find_all("table", class_="d_book")
        for div_tags in table_tags.find_all("div", class_="bookimage")
        for book_tags in div_tags.find_all("a")
    ]

    return books_id


def main():
    fiction_category_url = "http://tululu.org/l55"
    pages = 4
    for page in range(1, pages + 1):
        fiction_category_url = f"http://tululu.org/l55/{page}/"
        response = requests.get(fiction_category_url)
        response.raise_for_status()
        books_id = get_books_id(response)
        for book_id in books_id:
            book_url = urljoin(fiction_category_url, book_id)
            print(book_url)


if __name__ == "__main__":
    main()
