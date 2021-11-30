import json

from jinja2 import Environment, FileSystemLoader, select_autoescape


def main():
    fiction_books_attributes_file = "fiction_books.json"

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template("template.html")

    with open(fiction_books_attributes_file, "r") as my_file:
        books_json = my_file.read()

    books = json.loads(books_json)

    rendered_page = template.render(books=books)

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == "__main__":
    main()
