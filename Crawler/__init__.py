# __init__.py
# Diese Datei markiert das Verzeichnis 'Crawler' als ein Python-Package.
# Sie wird automatisch ausgeführt, wenn das Package importiert wird.

# Die __all__-Liste definiert die öffentlichen Schnittstellen des Packages.
# Beim Importieren mit 'from Crawler import *' werden nur die hier gelisteten Module (oder Namen) importiert.
# Dies hilft, die API des Packages klar zu definieren und ungewollte Imports zu vermeiden.
__all__ = ["CrawledArticle", "ArticleFetcher"]

# Importiert die Klasse CrawledArticle direkt in den Namespace des Packages.
# Dies ermöglicht den Zugriff auf CrawledArticle direkt über 'Crawler.CrawledArticle',
# anstatt 'Crawler.CrawledArticle.CrawledArticle' schreiben zu müssen.
from .CrawledArticle import CrawledArticle

# Importiert die Klasse ArticleFetcher direkt in den Namespace des Packages.
# Ähnlich wie bei CrawledArticle, um den Zugriff über 'Crawler.ArticleFetcher' zu vereinfachen.
from .ArticleFetcher import ArticleFetcher

