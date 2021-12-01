import json
import math
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload(file):
    books_on_page = 10
    pages_folder_name = "pages/"

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template("template.html")

    with open(file, "r") as books_atributes_json:
        books_json = books_atributes_json.read()

    books_atributes = json.loads(books_json)

    pages_count = math.ceil(len(books_atributes) / books_on_page)

    os.makedirs(pages_folder_name, exist_ok=True)
    books = chunked(books_atributes, books_on_page)

    for i, paged_books in enumerate(books, 1):
        index_file_path = os.path.join(pages_folder_name, f"index{i}.html")

        rendered_page = template.render(
            books=chunked(paged_books, 2),
            pages_count=pages_count,
            page_number=i,
        )

        with open(index_file_path, "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    fiction_books_attributes_file = "fiction_books.json"

    server = Server()

    server.watch(
        fiction_books_attributes_file, on_reload(fiction_books_attributes_file)
    )

    server.serve(root=".")


if __name__ == "__main__":
    main()
