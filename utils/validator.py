import re

REQUIRED_FIELDS = [
    "bid_number",
    "title",
    "due_date",
    "company_name"
]


def validate_extraction(data: dict) -> dict:
    issues = []

    for field in REQUIRED_FIELDS:
        if not data.get(field):
            issues.append(f"MISSING required field: {field}")

    due_date = data.get("due_date", "") or ""

    date_pattern = re.compile(
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
        r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)",
        re.IGNORECASE
    )

    if due_date and not date_pattern.search(due_date):
        issues.append(f'due_date may not be valid: "{due_date}"')

    null_fields = [
        key for key, value in data.items()
        if value is None and key not in REQUIRED_FIELDS
    ]

    if null_fields:
        issues.append(f"Fields not found in document: {null_fields}")

    return {
        "is_valid": not any(issue.startswith("MISSING") for issue in issues),
        "issues": issues
    }