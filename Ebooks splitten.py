import os
from pathlib import Path
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup


def split_epub_into_blocks(base_path, words_per_block=5000):
    path = Path(base_path)

    for epub_file in path.rglob('*.epub'):
        if "_split" in epub_file.name:
            continue

        print(f"Verarbeite: {epub_file.name}")

        try:
            book = epub.read_epub(str(epub_file))
            full_text = []

            # Wir suchen jetzt breiter nach Inhalten
            for item in book.get_items():
                # Nur Dokumente (HTML/XHTML) verarbeiten
                if item.get_type() == ITEM_DOCUMENT:
                    content = item.get_content()
                    if content:
                        soup = BeautifulSoup(content, 'html.parser')
                        # Wir entfernen Skripte und Styles, falls vorhanden
                        for script_or_style in soup(["script", "style"]):
                            script_or_style.decompose()

                        text = soup.get_text(separator=' ', strip=True)
                        if text:
                            full_text.append(text)

            if not full_text:
                print(f" WARNUNG: Kein Text in {epub_file.name} gefunden!")
                continue

            all_words = " ".join(full_text).split()
            print(f" - Wörter gefunden: {len(all_words)}")

            if len(all_words) == 0:
                continue

            blocks = []
            for i in range(0, len(all_words), words_per_block):
                block_content = " ".join(all_words[i:i + words_per_block])
                blocks.append(block_content)

            output_file = epub_file.with_name(f"{epub_file.stem}_split.txt")

            with open(output_file, 'w', encoding='utf-8') as f:
                for idx, block in enumerate(blocks):
                    f.write(f"--- KAPITEL {idx + 1} ---\n")
                    f.write(block)
                    f.write("\n\n")

            print(f" ERGEBNIS: {output_file.name} erstellt.")

        except Exception as e:
            print(f" FEHLER bei {epub_file.name}: {e}")


# Dein Pfad
target_path = r"d:\extracted\Verschiedene Dateien\Goldberg, Lee"
split_epub_into_blocks(target_path)