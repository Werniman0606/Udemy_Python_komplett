import os
from pydub import AudioSegment
from ShazamAPI import Shazam
from tqdm import tqdm
import csv

# --- KONFIGURATION ---
INPUT_FOLDER = r"D:\Test"
OUTPUT_CSV = os.path.join(INPUT_FOLDER, "playlist_ergebnisse.csv")
INTERVAL_MS = 4 * 60 * 1000  # 4 Minuten in Millisekunden
SAMPLE_DURATION_MS = 15000  # 15 Sekunden Schnipsel
RETRY_OFFSET_MS = 30000  # Bei "Kein Treffer" 30 Sek weiterhüpfen
VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.mpg', '.mpeg')


def recognize_audio(sample_path):
    """Schickt den Schnipsel synchron an Shazam."""
    try:
        with open(sample_path, 'rb') as f:
            mp3_file_content_to_recognize = f.read()

        shazam = Shazam(mp3_file_content_to_recognize)
        recognize_generator = shazam.recognizeSong()

        # Generator anstoßen und ersten Treffer abgreifen
        result = next(recognize_generator)

        if result and len(result) > 1:
            track_data = result[1]
            if track_data.get('track'):
                title = track_data['track']['title']
                artist = track_data['track']['subtitle']
                return f"{artist} - {title}"
    except Exception as e:
        # Falls der Generator leer ist oder ein Fehler auftritt, ignorieren
        pass
    return None


def format_timestamp(ms):
    """Rechnet Millisekunden in ein lesbares MM:SS Format um."""
    seconds = int((ms / 1000) % 60)
    minutes = int((ms / (1000 * 60)) % 60)
    hours = int((ms / (1000 * 60 * 60)) % 24)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def process_video_files():
    video_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(VIDEO_EXTENSIONS)]

    if not video_files:
        print(f"Keine passenden Videodateien in {INPUT_FOLDER} gefunden!")
        return

    print(f"Gefundene Dateien: {len(video_files)}")

    with open(OUTPUT_CSV, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Datei', 'Zeitstempel', 'Erkanntes Lied'])

        for file_name in video_files:
            file_path = os.path.join(INPUT_FOLDER, file_name)
            print(f"\nVerarbeite: {file_name}")
            print("Lade Audio-Spur...")

            try:
                audio = AudioSegment.from_file(file_path)
            except Exception as e:
                print(f"Fehler beim Laden: {e}")
                continue

            duration_ms = len(audio)
            print(f"Länge des Videos: {format_timestamp(duration_ms)}")

            current_time = 0

            with tqdm(total=duration_ms, unit="ms", desc="Scanne Video") as pbar:
                while current_time < duration_ms:
                    end_time = min(current_time + SAMPLE_DURATION_MS, duration_ms)
                    sample = audio[current_time:end_time]

                    temp_sample_path = "temp_shazam_sample.mp3"
                    sample.export(temp_sample_path, format="mp3")

                    result = recognize_audio(temp_sample_path)

                    # Retry-Logik (Moderator-Ausweich-Manöver)
                    if not result and (current_time + RETRY_OFFSET_MS + SAMPLE_DURATION_MS) < duration_ms:
                        retry_time = current_time + RETRY_OFFSET_MS
                        retry_end = retry_time + SAMPLE_DURATION_MS
                        retry_sample = audio[retry_time:retry_end]
                        retry_sample.export(temp_sample_path, format="mp3")
                        result = recognize_audio(temp_sample_path)

                    if os.path.exists(temp_sample_path):
                        os.remove(temp_sample_path)

                    display_time = format_timestamp(current_time)
                    final_result = result if result else "Kein Treffer / Sprache"

                    writer.writerow([file_name, display_time, final_result])
                    csv_file.flush()

                    pbar.update(INTERVAL_MS)
                    current_time += INTERVAL_MS

    print(f"\nFertig! Ergebnisse unter '{OUTPUT_CSV}'.")


if __name__ == "__main__":
    process_video_files()