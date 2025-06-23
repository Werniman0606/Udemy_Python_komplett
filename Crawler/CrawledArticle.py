class CrawledArticle():
    """
    Ein einfacher Datencontainer zur Repräsentation eines einzelnen Artikels,
    der von der Webseite gecrawlt wurde.

    Diese Klasse kapselt alle relevanten Informationen eines Artikels,
    um eine strukturierte und leicht handhabbare Datenform zu bieten.
    """
    def __init__(self, title, emoji, content, image):
        """
        Initialisiert ein neues CrawledArticle-Objekt mit den extrahierten Daten.

        Args:
            title (str): Der Titel des Artikels.
            emoji (str): Ein Emoji-Zeichen, das dem Artikel zugeordnet ist (z.B. als Kategorie-Indikator).
            content (str): Der Haupttextinhalt des Artikels.
            image (str): Die absolute URL zu einem Bild, das zum Artikel gehört.
                         Stellt sicher, dass das Bild direkt erreichbar ist.
        """
        self.title = title      # Speichert den Titel des Artikels.
        self.emoji = emoji      # Speichert das assoziierte Emoji.
        self.content = content  # Speichert den vollständigen Textinhalt des Artikels.
        self.image = image      # Speichert die vollständige (absolute) URL des Artikelbildes.