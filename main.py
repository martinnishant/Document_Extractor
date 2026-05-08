import json
from pathlib import Path

from parsers.pdf_parser import extract_text_from_pdf
from parsers.html_parser import extract_text_from_html
from extractor.llm_extractor import extract_rfp_fields
from utils.validator import validate_extraction

DOCUMENTS_DIR = Path("documents")
OUTPUT_FILE = Path("output/output.json")
SUPPORTED_EXTENSIONS = {".pdf", ".html", ".htm"}


def process_document(file_path: Path) -> dict:
    ext = file_path.suffix.lower()

    print(f"\nProcessing: {file_path}")

    if ext == ".pdf":
        text = extract_text_from_pdf(str(file_path))
    elif ext in {".html", ".htm"}:
        text = extract_text_from_html(str(file_path))
    else:
        return {}

    fields = extract_rfp_fields(text)

    fields["source_file"] = file_path.name
    fields["source_path"] = str(file_path)
    fields["bid_folder"] = file_path.parent.name
    fields["document_type"] = "addendum" if "addendum" in file_path.name.lower() else "rfp"

    fields["_validation"] = validate_extraction(fields)

    return fields


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    files = [
        file for file in DOCUMENTS_DIR.rglob("*")
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files:
        print("No PDF or HTML files found inside documents/")
        return

    print(f"Found {len(files)} document(s).")

    results = []

    for file_path in sorted(files):
        try:
            result = process_document(file_path)
            if result:
                results.append(result)
        except Exception as error:
            print(f"Failed to process {file_path}: {error}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print(f"\nDone. Output saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()