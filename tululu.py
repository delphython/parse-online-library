import requests
from bs4 import BeautifulSoup


url = "http://tululu.org/b1/"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "lxml")
title_tag = soup.find("head").find("title")
title_text = title_tag.text
heading_author, _, _ = title_text.split(",")
heading, author = heading_author.split("-")
print(f"Заголовок: {heading.strip()}")
print(f"Автор: {author.strip()}")
