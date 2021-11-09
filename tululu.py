import requests
from bs4 import BeautifulSoup


url = "http://tululu.org/b1/"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "lxml")
title_tag = soup.find("h1")
title_text = title_tag.text
print(title_text)
heading, author = title_text.split("::")
print(f"Заголовок: {heading.strip()}")
print(f"Автор: {author.strip()}")
