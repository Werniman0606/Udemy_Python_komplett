# Es ist zu empfehlen, hier mit Objektorientierung zu arbeiten
import requests
r = requests.get("http://python.beispiel.programmierenlernen.io/index.php")
from bs4 import BeautifulSoup
doc = BeautifulSoup(r.text, "html.parser")

class CrawledArticle():
    def __init__(self,title,emoji,content,image):
        self.title = title
        self.emoji = emoji
        self.content = content
        self.image = image

for card in doc.select(".card"):
    emoji = card.select_one(".emoji").text
    content = card.select_one(".card-text").text
    title = card.select(".card-title span")[1].text
    image = card.select_one("img").attrs["src"]

    crawled

    print(image)
    print(emoji)
    print(content)
    print(title)
    break
