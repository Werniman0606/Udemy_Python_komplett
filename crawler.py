import Crawler
fetcher=Crawler.ArticleFetcher()
for element in fetcher.fetch():
    print(element.emoji + ": " + element.title)