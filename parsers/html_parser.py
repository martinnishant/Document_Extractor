from bs4 import BeautifulSoup
from pathlib import Path

NOISE_TAGS = [
    'script', 'style', 'nav', 'footer', 'header',
    'aside', 'noscript', 'iframe', 'meta', 'link'
]


def extract_text_from_html(html_path: str) -> str:

    path = Path(html_path)

    if not path.exists():
        raise FileNotFoundError(f'HTML file not found: {html_path}')

    with open(html_path, 'r', encoding='utf-8', errors='ignore') as file:
        raw_html = file.read()

    soup = BeautifulSoup(raw_html, 'html.parser')

    for tag in soup(NOISE_TAGS):
        tag.decompose()

    for table in soup.find_all('table'):
        rows = []

        for tr in table.find_all('tr'):
            cells = [
                cell.get_text(strip=True)
                for cell in tr.find_all(['td', 'th'])
            ]

            if any(cells):
                rows.append(' | '.join(cells))

        table.replace_with(soup.new_string('\n'.join(rows)))

    text = soup.get_text(separator='\n')

    lines = [line.strip() for line in text.splitlines()]
    clean_lines = [line for line in lines if line and len(line) > 2]

    return '\n'.join(clean_lines)