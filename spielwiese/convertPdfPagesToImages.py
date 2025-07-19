import os
from pdf2image import convert_from_path

# Pfad zum Ordner, der alle PDF-Dateien enthält
BASE_FOLDER = r"/Users/mh/Documents/SICK/PerformanceDialog/2025/Pdfs"


def process_pdf(pdf_path, base_folder):
    try:
        # Alle Seiten des PDFs in eine Liste von PIL-Image-Objekten konvertieren
        images = convert_from_path(pdf_path)

        # Basis-Dateiname ohne Erweiterung
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Unterordner erstellen, benannt wie die PDF-Datei, im BASE_FOLDER
        output_folder = os.path.join(base_folder, pdf_name)
        os.makedirs(output_folder, exist_ok=True)

        # Jede Seite als PNG speichern: Dqateiname = pdf_name + fortlaufende Nummer
        for idx, img in enumerate(images, start=1):
            output_file = os.path.join(output_folder, f"{pdf_name}_{idx}.png")
            img.save(output_file, "PNG")
            print(
                f"PDF '{pdf_name}': Seite {idx} gespeichert unter {output_file}")

    except Exception as e:
        print(f"Fehler bei der Verarbeitung von {pdf_path}: {e}")


def process_all_pdfs(folder):
    # Alle Dateien im Ordner durchgehen und PDF-Dateien verarbeiten
    for file in os.listdir(folder):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder, file)
            process_pdf(pdf_path, folder)


if __name__ == "__main__":
    process_all_pdfs(BASE_FOLDER)
