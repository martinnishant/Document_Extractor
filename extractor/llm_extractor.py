import json
import os
from groq import Groq
from dotenv import load_dotenv
from utils.chunker import chunk_text

load_dotenv()

FIELDS = [
    "bid_number",
    "title",
    "due_date",
    "bid_submission_type",
    "term_of_bid",
    "pre_bid_meeting",
    "installation",
    "bid_bond_requirement",
    "delivery_date",
    "payment_terms",
    "additional_documentation",
    "mfg_for_registration",
    "contract_or_cooperative",
    "model_no",
    "part_no",
    "product",
    "contact_info",
    "company_name",
    "bid_summary",
    "product_specification"
]

LIST_FIELDS = {
    "additional_documentation",
    "model_no",
    "part_no",
    "product",
    "product_specification"
}

SYSTEM_PROMPT = """
You are an expert procurement and RFP document analyst.

Your task is to extract structured information from RFPs, bids, tenders,
contracts, affidavits, quotations, and addendum documents.

Return ONLY one valid JSON object with these exact keys:

bid_number
title
due_date
bid_submission_type
term_of_bid
pre_bid_meeting
installation
bid_bond_requirement
delivery_date
payment_terms
additional_documentation
mfg_for_registration
contract_or_cooperative
model_no
part_no
product
contact_info
company_name
bid_summary
product_specification

STRICT RULES:
- Return raw JSON only
- Do not use markdown
- Do not explain anything
- Never invent values
- Extract only information explicitly present in the document
- If a field is missing, return null
- Do not omit any key
- Keep extracted values concise and accurate
- company_name must be the issuing organization or vendor clearly mentioned
- contact_info should contain real contact details only
- bid_summary should be a short 2-3 sentence summary

LIST FIELDS:
Return these fields as arrays:
- additional_documentation
- model_no
- part_no
- product
- product_specification
"""


def empty_result() -> dict:
    return {field: None for field in FIELDS}


def clean_json_response(raw: str) -> str:
    raw = raw.strip()

    if raw.startswith("```"):
        raw = raw.replace("```json", "")
        raw = raw.replace("```", "")
        raw = raw.strip()

    start = raw.find("{")
    end = raw.rfind("}")

    if start != -1 and end != -1:
        raw = raw[start:end + 1]

    return raw


def call_groq(chunk: str, client: Groq) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=2048,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"Extract the required RFP fields from this text:\n\n{chunk}"
            }
        ]
    )

    raw = response.choices[0].message.content
    cleaned = clean_json_response(raw)

    return json.loads(cleaned)


def merge_results(results: list[dict]) -> dict:
    merged = empty_result()

    for result in results:
        for field in FIELDS:
            value = result.get(field)

            if value is None or value == "":
                continue

            if field in LIST_FIELDS:
                existing = merged[field] or []

                if isinstance(value, list):
                    for item in value:
                        if item and item not in existing:
                            existing.append(item)

                elif isinstance(value, str):
                    if value not in existing:
                        existing.append(value)

                merged[field] = existing if existing else None

            else:
                if merged[field] is None:
                    merged[field] = value

    return merged


def extract_rfp_fields(text: str) -> dict:
    if not text or not text.strip():
        return empty_result()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Add it inside your .env file.")

    client = Groq(api_key=api_key)
    chunks = chunk_text(text)

    results = []

    for index, chunk in enumerate(chunks, start=1):
        print(f"Processing chunk {index}/{len(chunks)}")

        try:
            result = call_groq(chunk, client)
            results.append(result)

        except json.JSONDecodeError:
            print(f"Warning: chunk {index} returned invalid JSON")

        except Exception as error:
            print(f"Warning: chunk {index} failed: {error}")

    if not results:
        return empty_result()

    return merge_results(results)