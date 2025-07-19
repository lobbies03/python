import os
import re
import sys
import time
import PyPDF2
import subprocess
from datetime import datetime


def extract_text_from_pdf(pdf_path):
    """Extrahiert den Text aus einer PDF-Datei."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Fehler beim Lesen von {pdf_path}: {e}")
    return text


def extract_dates(text):
    """Extrahiert alle Datumsangaben und konvertiert sie ins Format YYYY-MM-DD."""
    # Verbesserte Regex-Muster für Datumssuche
    patterns = [
        # Deutsches Format mit Punkten (DD.MM.YYYY)
        r'(\d{1,2}[\.\s]+\d{1,2}[\.\s]+\d{4})',

        # Deutsches Format mit Wörtern wie "Rechnungsdatum", "Datum", "vom"
        r'(?:Rechnungsdatum|Datum|vom|Date)[\s:]*(\d{1,2}[\.\s]+\d{1,2}[\.\s]+\d{4})',

        # ISO-Format (YYYY-MM-DD)
        r'(\d{4}-\d{1,2}-\d{1,2})',

        # Format mit Schrägstrichen (DD/MM/YYYY)
        r'(\d{1,2}/\d{1,2}/\d{4})',

        # Datumformat mit Monatsnamen (z.B. 15. Januar 2023)
        r'(\d{1,2}[\.\s]+(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)[\s]+\d{4})',
        r'(\d{1,2}[\.\s]+(Jan|Feb|Mär|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Dez)[\s]+\d{4})'
    ]

    # Sammele alle gefundenen Datumsangaben
    all_dates = []
    for pattern in patterns:
        found_dates = re.findall(pattern, text, re.IGNORECASE)
        all_dates.extend(found_dates)

    # Verarbeite gefundene Daten und entferne Duplikate
    processed_dates = []
    for date_item in all_dates:
        # Handle Tuples (captured groups)
        if isinstance(date_item, tuple):
            date_item = date_item[0]
        date_item = date_item.strip()
        processed_dates.append(date_item)

    unique_dates = list(set(processed_dates))

    # Konvertiere alle Datumsformate in ein einheitliches Format (YYYY-MM-DD)
    formatted_dates = []

    # Monatsnamenmapping
    month_names = {
        'januar': '01', 'jan': '01',
        'februar': '02', 'feb': '02',
        'märz': '03', 'mär': '03', 'march': '03', 'mar': '03',
        'april': '04', 'apr': '04',
        'mai': '05', 'may': '05',
        'juni': '06', 'jun': '06', 'june': '06',
        'juli': '07', 'jul': '07', 'july': '07',
        'august': '08', 'aug': '08',
        'september': '09', 'sep': '09',
        'oktober': '10', 'okt': '10', 'october': '10', 'oct': '10',
        'november': '11', 'nov': '11',
        'dezember': '12', 'dez': '12', 'december': '12', 'dec': '12'
    }

    for date_str in unique_dates:
        try:
            # Bereinige Datumszeichenkette
            date_str = re.sub(r'\s+', ' ', date_str).strip()

            # Deutsches Format mit Punkten (DD.MM.YYYY)
            if re.match(r'\d{1,2}\.\d{1,2}\.\d{4}', date_str):
                day, month, year = date_str.split('.')
                formatted_date = f"{year.strip()}-{month.strip().zfill(2)}-{day.strip().zfill(2)}"
                formatted_dates.append(formatted_date)

            # ISO-Format (YYYY-MM-DD) - bereits im richtigen Format
            elif re.match(r'\d{4}-\d{1,2}-\d{1,2}', date_str):
                # Stelle sicher, dass Monat und Tag zweistellig sind
                year, month, day = date_str.split('-')
                formatted_date = f"{year.strip()}-{month.strip().zfill(2)}-{day.strip().zfill(2)}"
                formatted_dates.append(formatted_date)

            # Format mit Schrägstrichen (DD/MM/YYYY) -> umwandeln in YYYY-MM-DD
            elif re.match(r'\d{1,2}/\d{1,2}/\d{4}', date_str):
                day, month, year = date_str.split('/')
                formatted_date = f"{year.strip()}-{month.strip().zfill(2)}-{day.strip().zfill(2)}"
                formatted_dates.append(formatted_date)

            # Datumformat mit Monatsnamen (z.B. 15. Januar 2023)
            elif re.match(r'\d{1,2}[\.\s]+(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember|Jan|Feb|Mär|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Dez)[\s]+\d{4}', date_str, re.IGNORECASE):
                parts = re.split(r'[\.\s]+', date_str.strip())
                day = parts[0].zfill(2)
                month_name = parts[1].lower()
                year = parts[-1]

                if month_name in month_names:
                    month = month_names[month_name]
                    formatted_date = f"{year}-{month}-{day}"
                    formatted_dates.append(formatted_date)

            # Versuche zusätzliche Formate zu erkennen
            else:
                # Format mit Leerzeichen statt Punkten (DD MM YYYY)
                if re.match(r'\d{1,2}\s+\d{1,2}\s+\d{4}', date_str):
                    parts = date_str.split()
                    day, month, year = parts[0], parts[1], parts[2]
                    formatted_date = f"{year.strip()}-{month.strip().zfill(2)}-{day.strip().zfill(2)}"
                    formatted_dates.append(formatted_date)
        except Exception as e:
            print(f"Fehler bei der Datumskonvertierung für {date_str}: {e}")

    return formatted_dates


def open_pdf(file_path):
    """Öffnet die PDF-Datei mit dem Standardprogramm des Betriebssystems."""
    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
            return True
        elif os.name == 'posix':  # macOS und Linux
            if sys.platform == 'darwin':  # macOS
                subprocess.call(('open', file_path))
                return True
            else:  # Linux
                subprocess.call(('xdg-open', file_path))
                return True
        else:
            print(
                f"Konnte die Datei nicht automatisch öffnen: Nicht unterstütztes Betriebssystem.")
            return False
    except Exception as e:
        print(f"Fehler beim Öffnen der PDF: {e}")
        return False


def user_selection(options, selection_type, default=None):
    """Lässt den Benutzer eine Option auswählen."""
    if not options:
        return default

    print(f"\nBitte wählen Sie {selection_type} aus:")
    for i, option in enumerate(options):
        print(f"{chr(97 + i)}) {option}")

    if default:
        print(f"\nOder drücken Sie Enter für Manuell eingeben")

    while True:
        choice = input("\nWählen Sie (a, b, c, ...): ").strip().lower()

        if not choice and default:
            return default

        if choice and ord(choice) - ord('a') < len(options) and ord(choice) >= ord('a'):
            return options[ord(choice) - ord('a')]
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")


def manual_input(prompt):
    """Ermöglicht manuelle Eingabe."""
    return input(prompt).strip()


def process_pdf_files(folder_path):
    """Verarbeitet alle PDF-Dateien im angegebenen Ordner."""
    if not os.path.exists(folder_path):
        print(f"Der Ordner {folder_path} existiert nicht.")
        return

    pdf_files = [f for f in os.listdir(
        folder_path) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"Keine PDF-Dateien im Ordner {folder_path} gefunden.")
        return

    # Identifiziere Dateien, die bereits dem Muster YYYY-MM-DD_ entsprechen
    processed_files = []
    unprocessed_files = []
    for pdf_file in pdf_files:
        if re.match(r'\d{4}-\d{2}-\d{2}_', pdf_file):
            processed_files.append(pdf_file)
        else:
            unprocessed_files.append(pdf_file)

    # Zeige Status an
    print(f"Gefunden: {len(pdf_files)} PDF-Dateien insgesamt")
    print(f"- {len(unprocessed_files)} Dateien ohne Datum im Namen")
    print(f"- {len(processed_files)} Dateien mit Datum bereits im Namen")

    # Frage, ob bereits verarbeitete Dateien überprüft werden sollen
    include_processed = False
    if processed_files:
        reprocess = input(
            "\nMöchten Sie auch Dateien, die bereits ein Datum im Namen haben, erneut durchgehen? (j/n): ").strip().lower()
        include_processed = reprocess == 'j'

    # Bestimme die Liste der zu verarbeitenden Dateien
    files_to_process = unprocessed_files.copy()
    if include_processed:
        files_to_process.extend(processed_files)

    if not files_to_process:
        print("Keine Dateien zum Verarbeiten.")
        return

    print(f"\nEs werden {len(files_to_process)} Dateien verarbeitet.")

    results = {}
    skipped_files = []

    for pdf_file in files_to_process:
        file_path = os.path.join(folder_path, pdf_file)
        print(f"\n{'='*50}")
        print(f"Verarbeite: {pdf_file}")
        print(f"{'='*50}")

        # Prüfe, ob die Datei bereits ein Datum im Namen hat
        already_processed = re.match(r'\d{4}-\d{2}-\d{2}_', pdf_file)
        if already_processed:
            process_file = input(
                "Diese Datei wurde bereits bearbeitet. Möchten Sie sie erneut bearbeiten? (j/n): ").strip().lower()
            if process_file != 'j':
                print(f"Überspringe: {pdf_file}")
                skipped_files.append(pdf_file)
                continue

        # Öffne die PDF-Datei
        pdf_opened = open_pdf(file_path)
        if not pdf_opened:
            print("Konnte die PDF nicht öffnen. Verarbeitung wird trotzdem fortgesetzt.")
        else:
            print("PDF wurde geöffnet. Bitte prüfen Sie das Dokument.")
            print(
                "Sobald Sie es geprüft haben, schließen Sie es und kehren Sie zu diesem Terminal zurück.")

        # Text aus PDF extrahieren
        text = extract_text_from_pdf(file_path)

        # Datumsangaben extrahieren
        dates = extract_dates(text)
        date_to_use = None

        # Wenn die Datei bereits ein Datum im Namen hat, füge dieses als Option hinzu
        existing_date = None
        if already_processed:
            # Extrahiere YYYY-MM-DD aus dem Dateinamen
            existing_date = pdf_file[:10]
            if existing_date not in dates and re.match(r'\d{4}-\d{2}-\d{2}', existing_date):
                dates.append(existing_date)
                print(f"Vorhandenes Datum im Dateinamen: {existing_date}")

        if not dates:
            print("Kein Datum gefunden.")
            date_to_use = manual_input(
                "Bitte geben Sie ein Datum im Format JJJJ-MM-TT ein: ")
        else:
            # Füge "Manuell eingeben" als Option hinzu
            dates.append("*** Manuell eingeben ***")
            print("Folgende Datumsangaben wurden gefunden:")
            date_to_use = user_selection(dates, "ein Datum", existing_date)

            # Wenn "Manuell eingeben" ausgewählt wurde
            if date_to_use == "*** Manuell eingeben ***":
                date_to_use = manual_input(
                    "Bitte geben Sie ein Datum im Format JJJJ-MM-TT ein: ")

        # Stelle sicher, dass das Datum im YYYY-MM-DD Format ist
        # DD.MM.YYYY
        if date_to_use and re.match(r'\d{2}\.\d{2}\.\d{4}', date_to_use):
            day, month, year = date_to_use.split('.')
            date_to_use = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

        # Extrahiere ggf. vorhandenen Beschreibungstext aus dem Dateinamen
        existing_text = ""
        if already_processed:
            # Extrahiere alles nach dem Datum und vor der Dateiendung
            file_base = os.path.splitext(pdf_file)[0]  # Name ohne Erweiterung
            existing_text = file_base[11:]  # Text nach YYYY-MM-DD_

        # Frage nach einem benutzerdefinierten Text
        if existing_text:
            print(f"Aktueller Beschreibungstext: {existing_text}")
            custom_text = manual_input(
                f"Bitte geben Sie einen neuen Text ein (oder Enter für '{existing_text}'): ")
            if not custom_text.strip():
                custom_text = existing_text
        else:
            custom_text = manual_input(
                "\nBitte geben Sie einen Text ein, der nach dem Datum folgen soll: ")

        # Bereinige den benutzerdefinierten Text für die Verwendung im Dateinamen
        custom_text = re.sub(r'[\\/*?:"<>|]', '', custom_text)

        if date_to_use and custom_text:
            results[pdf_file] = (date_to_use, custom_text)
            print(
                f"Für {pdf_file} wurde das Datum {date_to_use} und der Text '{custom_text}' ausgewählt.")
        else:
            print(
                f"Für {pdf_file} wurden keine ausreichenden Informationen gesammelt.")

    # Ergebnisse anzeigen
    if results:
        print("\n" + "="*50)
        print("Zusammenfassung der Ergebnisse:")
        print("="*50)
        for pdf_file, (date, text) in results.items():
            new_name = f"{date}_{text}{os.path.splitext(pdf_file)[1]}"
            print(f"{pdf_file} -> {new_name}")

        # Frage, ob die Dateien umbenannt werden sollen
        rename = input(
            "\nMöchten Sie die Dateien mit dem ausgewählten Datum und Text umbenennen? (j/n): ").strip().lower()
        if rename == 'j':
            for pdf_file, (date, text) in results.items():
                old_path = os.path.join(folder_path, pdf_file)

                # Extrahiere die Dateiendung
                file_extension = os.path.splitext(pdf_file)[1]

                # Erstelle neuen Dateinamen im Format YYYY-MM-DD_Benutzerdefinierter-Text.pdf
                new_filename = f"{date}_{text}{file_extension}"
                new_path = os.path.join(folder_path, new_filename)

                # Prüfe, ob die Datei bereits so heißt
                if pdf_file == new_filename:
                    print(
                        f"Übersprungen: {pdf_file} (Dateiname bereits korrekt)")
                    continue

                # Prüfe, ob eine Datei mit dem neuen Namen bereits existiert
                if os.path.exists(new_path) and old_path != new_path:
                    overwrite = input(
                        f"Eine Datei mit dem Namen {new_filename} existiert bereits. Überschreiben? (j/n): ").strip().lower()
                    if overwrite != 'j':
                        print(f"Übersprungen: {pdf_file}")
                        continue

                try:
                    os.rename(old_path, new_path)
                    print(f"Umbenannt: {pdf_file} -> {new_filename}")
                except Exception as e:
                    print(f"Fehler beim Umbenennen von {pdf_file}: {e}")

    # Zusammenfassung anzeigen
    files_processed = len(results)
    files_skipped = len(skipped_files)
    print("\n" + "="*50)
    print(f"Gesamtzusammenfassung:")
    print(f"- {files_processed} Dateien verarbeitet")
    print(f"- {files_skipped} Dateien übersprungen")
    print("="*50)


if __name__ == "__main__":
    print("=" * 60)
    print("PDF-Rechnungen Datumsextraktionstool")
    print("=" * 60)
    print("Dieses Tool öffnet PDF-Dateien und hilft Ihnen, Datumsangaben zu extrahieren.")
    print("Die Dateien werden im Format JJJJ-MM-TT_Beschreibungstext.pdf umbenannt.")
    print("Für jede PDF werden die gefundenen Datumsangaben angezeigt, nachdem Sie die Datei geprüft haben.")
    print()

    folder_path = input(
        "Bitte geben Sie den Pfad zum Ordner mit den PDF-Rechnungen ein: ")
    process_pdf_files(folder_path.strip())

    print("\nProzess abgeschlossen.")
    input("Drücken Sie die Eingabetaste, um das Programm zu beenden...")
