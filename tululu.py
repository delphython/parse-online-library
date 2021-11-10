import requests
from bs4 import BeautifulSoup


url = "http://tululu.org/b9/"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "lxml")
title_tag = soup.find("h1")
title_text = title_tag.text
heading, author = title_text.split("::")
print(f"Заголовок: {heading.strip()}")
print(f"Автор: {author.strip()}")

img = soup.find("div", class_="bookimage").find("img")["src"]
print(img)

comments = soup.find_all("div", class_="texts")
for comment in comments:
    c = comment.find("span")
    print(c.text)
