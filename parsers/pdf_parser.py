import pdfplumber
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f'PDF not found: {pdf_path}')

    full_text = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_num, page in enumerate(pdf.pages, start=1):

            text = page.extract_text()

            if text and text.strip():
                full_text.append(f'=== Page {page_num} ===')
                full_text.append(text.strip())

            tables = page.extract_tables()

            for table in tables:

                for row in table:

                    clean = [
                        str(cell).strip() if cell else ''
                        for cell in row
                    ]

                    row_text = ' | '.join(clean)

                    if row_text.replace('|', '').strip():
                        full_text.append(row_text)

    if not full_text:
        return ''

    return '\n'.join(full_text)