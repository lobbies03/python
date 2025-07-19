import os
import sys
from PyPDF2 import PdfReader


def convert_pdf_to_text(pdf_path, text_path):
    try:
        reader = PdfReader(pdf_path)
        text_content = []
        for page in reader.pages:
            text = page.extract_text()
            if text:  # Seite könnte leer sein
                text_content.append(text)

        with open(text_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(text_content))
        print(f"Konvertierung erfolgreich: {text_path}")
    except Exception as e:
        print(f"Fehler bei der Konvertierung von {pdf_path}: {e}")


def convert_all_pdfs_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        print("Ungültiger Ordnerpfad.")
        return

    # Unterordner für konvertierte Dateien erstellen
    output_folder = os.path.join(folder_path, "convertedPdfToTxtFiles")
    os.makedirs(output_folder, exist_ok=True)

    # Alle PDFs im Ordner einlesen
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            # Zielpfad im Unterordner
            text_filename = os.path.splitext(filename)[0] + ".txt"
            text_path = os.path.join(output_folder, text_filename)

            convert_pdf_to_text(pdf_path, text_path)


def main():
    if len(sys.argv) < 2:
        print("Aufruf: python scriptname.py <Ordnerpfad>")
        return

    folder_path = sys.argv[1]
    convert_all_pdfs_in_folder(folder_path)


if __name__ == "__main__":
    main()
