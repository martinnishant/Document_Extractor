# 📄 Document Extractor

An AI-powered CLI tool that automatically extracts structured procurement data from **RFP, bid, tender, and addendum documents** (PDF & HTML) using **Groq's LLaMA 3.3 70B** model — and outputs clean, validated JSON.

---

## ✨ Features

- 🔍 **Multi-format parsing** — Supports PDF (text + tables) and HTML documents
- 🤖 **LLM-powered extraction** — Uses `llama-3.3-70b-versatile` via Groq API to intelligently extract 19 structured fields
- 🧩 **Smart chunking** — Splits large documents into overlapping chunks so no context is lost
- 🔀 **Result merging** — Intelligently merges extractions across chunks, deduplicating list fields
- ✅ **Validation layer** — Flags missing required fields and suspicious date formats
- 📁 **Batch processing** — Recursively processes an entire `documents/` folder in one run
- 💾 **JSON output** — Saves all results to `output/output.json`

---

## 📦 Extracted Fields

| Field | Type | Description |
|---|---|---|
| `bid_number` | string | Unique bid/RFP identifier |
| `title` | string | Full title of the document |
| `due_date` | string | Submission deadline |
| `bid_submission_type` | string | Electronic, physical, etc. |
| `term_of_bid` | string | Contract duration |
| `pre_bid_meeting` | string | Pre-bid meeting details |
| `installation` | string | Installation requirements |
| `bid_bond_requirement` | string | Bond details if required |
| `delivery_date` | string | Expected delivery timeline |
| `payment_terms` | string | Payment schedule/terms |
| `additional_documentation` | array | List of required docs |
| `mfg_for_registration` | string | Manufacturer registration info |
| `contract_or_cooperative` | string | Contract/cooperative details |
| `model_no` | array | Product model numbers |
| `part_no` | array | Product part numbers |
| `product` | array | List of products |
| `contact_info` | string | Issuer contact details |
| `company_name` | string | Issuing organization |
| `bid_summary` | string | 2–3 sentence document summary |
| `product_specification` | array | Technical specifications |

---

## 🗂️ Project Structure

```
Document_Extractor/
│
├── documents/              # Place your PDF/HTML files here (supports subfolders)
│   └── Bid1/
│       ├── RFP.pdf
│       └── Addendum.pdf
│
├── output/
│   └── output.json         # Extracted results saved here
│
├── parsers/
│   ├── pdf_parser.py       # Extracts text + tables from PDFs via pdfplumber
│   └── html_parser.py      # Cleans and extracts text from HTML via BeautifulSoup
│
├── extractor/
│   └── llm_extractor.py    # Groq API integration + chunk merging logic
│
├── utils/
│   ├── chunker.py          # Splits text into overlapping word-level chunks
│   └── validator.py        # Validates required fields and date formats
│
├── main.py                 # CLI entry point — orchestrates the full pipeline
├── requirements.txt
├── .env                    # Your GROQ_API_KEY goes here
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Document_Extractor.git
cd Document_Extractor
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY="your_groq_api_key_here"
```

> Get a free API key at [console.groq.com](https://console.groq.com)

### 5. Add your documents

Place your `.pdf` or `.html` files inside the `documents/` folder. Subfolders are supported:

```
documents/
└── Bid1/
    ├── RFP JA-207652.pdf
    └── Addendum 1.pdf
```

### 6. Run the extractor

```bash
python main.py
```

---

## 📤 Output Format

Results are saved to `output/output.json` as a JSON array. Each entry corresponds to one document:

```json
[
  {
    "bid_number": "JA-207652",
    "title": "Student and Staff Computing Devices",
    "due_date": "June 15, 2025",
    "company_name": "ABC Unified School District",
    "product": ["Laptops", "Tablets"],
    "bid_summary": "This RFP solicits bids for student and staff computing devices...",
    "source_file": "RFP JA-207652.pdf",
    "source_path": "documents/Bid1/RFP JA-207652.pdf",
    "bid_folder": "Bid1",
    "document_type": "rfp",
    "_validation": {
      "is_valid": true,
      "issues": []
    }
  }
]
```

Each record also includes metadata fields automatically added by the pipeline:

| Field | Description |
|---|---|
| `source_file` | Filename of the processed document |
| `source_path` | Relative path to the document |
| `bid_folder` | Parent folder name (useful for grouping bid sets) |
| `document_type` | `"rfp"` or `"addendum"` (auto-detected from filename) |
| `_validation` | Validation report with `is_valid` flag and list of `issues` |

---

## ⚙️ Configuration

### Chunking

Large documents are split into chunks of **3,000 words** with a **400-word overlap** to preserve context across chunk boundaries. You can adjust these defaults in `utils/chunker.py`:

```python
def chunk_text(text, chunk_size=3000, overlap=400):
```

### LLM Model

The extractor uses `llama-3.3-70b-versatile` on Groq. To switch models, update `extractor/llm_extractor.py`:

```python
model="llama-3.3-70b-versatile"
```

---

## ⚠️ Rate Limits

Groq's free tier has token-per-day (TPD) limits. If you hit a rate limit, the tool will print a warning for that chunk and continue processing the rest:

```
Warning: chunk 2 failed: Error code: 429 - Rate limit reached...
```

To avoid this:
- Process fewer documents per run
- Upgrade to Groq's [Dev Tier](https://console.groq.com/settings/billing)
- Add a delay between API calls

---

## 🛠️ Dependencies

| Package | Purpose |
|---|---|
| `pdfplumber` | PDF text and table extraction |
| `beautifulsoup4` | HTML parsing and cleaning |
| `groq` | Groq API client for LLaMA inference |
| `python-dotenv` | Load environment variables from `.env` |

Install all with:

```bash
pip install -r requirements.txt
```

---

## 📋 Supported Document Types

- ✅ RFPs (Request for Proposals)
- ✅ Bids & Tenders
- ✅ Addenda
- ✅ Contracts & Affidavits
- ✅ Quotations

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
