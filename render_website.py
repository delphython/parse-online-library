import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload(file):
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template("template.html")

    with open(file, "r") as my_file:
        books_json = my_file.read()

    books = chunked(json.loads(books_json), 2)

    rendered_page = template.render(books=books)

    with open("index.html", "w", encoding="utf8") as file:
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
