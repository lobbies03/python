import os
import pdfplumber

# Pfad zum Ordner mit den PDFs
FOLDER_PATH = r"/Users/mh/Documents/SICK/PerformanceDialog/pdfFilesToConvert/"


def convert_pdf_to_text(pdf_path, text_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = []
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text.append(page_text)

        with open(text_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_text))

        print(f"Konvertierung erfolgreich: {text_path}")
    except Exception as e:
        print(f"Fehler bei der Konvertierung von {pdf_path}: {e}")


def convert_all_pdfs_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        print("Ungültiger Ordnerpfad:", folder_path)
        return

    script_name = os.path.splitext(os.path.basename(__file__))[
        0]  # Skriptname ohne .py
    output_folder = os.path.join(folder_path, script_name)
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            txt_name = os.path.splitext(filename)[0] + ".txt"
            text_path = os.path.join(output_folder, txt_name)

            convert_pdf_to_text(pdf_path, text_path)


if __name__ == "__main__":
    convert_all_pdfs_in_folder(FOLDER_PATH)
