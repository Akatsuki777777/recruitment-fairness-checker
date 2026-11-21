from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
from collections import defaultdict
from openpyxl import load_workbook
from pypdf import PdfReader
import csv
import io

BASE = Path(__file__).resolve().parent
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

REQUIRED = {"candidate_id", "group", "qualified", "selected"}
ALLOWED = {".csv", ".txt", ".xlsx", ".pdf"}


def parse_delimited(text):
    try:
        dialect = csv.Sniffer().sniff(text[:8192], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    return list(csv.reader(io.StringIO(text.lstrip("\ufeff")), dialect))


def read_file(upload):
    extension = Path(upload.filename or "").suffix.lower()
    raw = upload.read()

    if not raw:
        raise ValueError("The uploaded file is empty.")

    if extension == ".xlsx":
        workbook = load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
        rows = list(workbook.active.iter_rows(values_only=True))
        workbook.close()
        return rows

    if extension == ".pdf":
        reader = PdfReader(io.BytesIO(raw))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        if not text.strip():
            raise ValueError("No selectable text found. Scanned PDFs are not supported.")
        rows = parse_delimited(text)
        headers = {str(x).strip().lower() for x in rows[0] if x is not None}
        if not REQUIRED.issubset(headers):
            raise ValueError(
                "Could not detect a delimited table in this PDF. "
                "Export the table as CSV or XLSX for reliable analysis."
            )
        return rows

    if extension in {".csv", ".txt"}:
        try:
            return parse_delimited(raw.decode("utf-8-sig"))
        except UnicodeDecodeError:
            raise ValueError("Text files must use UTF-8 encoding.")

    raise ValueError("Supported formats: CSV, TXT, XLSX and PDF.")


def analyse(rows):
    if not rows:
        raise ValueError("The dataset is empty.")

    headers = [
        str(x).strip().lower() if x is not None else ""
        for x in rows[0]
    ]

    if not REQUIRED.issubset(headers):
        raise ValueError(
            "Missing required columns: candidate_id, group, qualified, selected."
        )

    indexes = {key: headers.index(key) for key in REQUIRED}
    groups = defaultdict(lambda: {
        "applicants": 0, "selected": 0,
        "qualified": 0, "qualified_selected": 0
    })
    seen = set()
    total = 0

    for line, row in enumerate(rows[1:], start=2):
        if not row or not any(str(v).strip() for v in row if v is not None):
            continue

        def cell(key):
            i = indexes[key]
            return str(row[i]).strip() if i < len(row) and row[i] is not None else ""

        candidate_id, group = cell("candidate_id"), cell("group")

        if not candidate_id or not group:
            raise ValueError(f"Missing candidate ID or group on row {line}.")
        if candidate_id in seen:
            raise ValueError(f"Duplicate candidate ID: {candidate_id}")
        seen.add(candidate_id)

        if cell("qualified") not in {"0", "1"} or cell("selected") not in {"0", "1"}:
            raise ValueError(f"Values must be 0 or 1 on row {line}.")

        qualified, selected = int(cell("qualified")), int(cell("selected"))

        if selected and not qualified:
            raise ValueError(f"Selected candidate is unqualified on row {line}.")

        g = groups[group]
        g["applicants"] += 1
        g["selected"] += selected
        g["qualified"] += qualified
        g["qualified_selected"] += selected
        total += 1

    if not total:
        raise ValueError("The dataset contains no candidate records.")

    results, all_rates, qualified_rates = [], {}, {}

    for name, g in sorted(groups.items()):
        all_rate = g["selected"] / g["applicants"]
        qualified_rate = (
            g["qualified_selected"] / g["qualified"] if g["qualified"] else None
        )
        all_rates[name] = all_rate
        if qualified_rate is not None:
            qualified_rates[name] = qualified_rate

        results.append({
            "group": name,
            **g,
            "all_rate": all_rate,
            "qualified_rate": qualified_rate,
            "small_sample": g["applicants"] < 30
        })

    def compare(rates):
        if len(rates) < 2:
            return {"message": "At least two groups with valid rates are needed."}

        low = min(rates, key=rates.get)
        high = max(rates, key=rates.get)

        if rates[high] == 0:
            return {"message": "No selections recorded; ratio cannot be calculated."}

        ratio = rates[low] / rates[high]
        return {
            "low_group": low,
            "high_group": high,
            "ratio": ratio,
            "message": (
                "Below optional 0.80 screening threshold"
                if ratio < 0.8
                else "At or above optional 0.80 screening threshold"
            )
        }

    selected_total = sum(g["selected"] for g in groups.values())

    return {
        "total": total,
        "group_count": len(groups),
        "selected_total": selected_total,
        "overall_rate": selected_total / total,
        "groups": results,
        "all_comparison": compare(all_rates),
        "qualified_comparison": compare(qualified_rates)
    }


@app.get("/")
def home():
    return send_from_directory(BASE, "index.html")


@app.post("/api/analyse")
def api_analyse():
    upload = request.files.get("file")
    if not upload:
        return jsonify({"error": "Choose a file first."}), 400

    if Path(upload.filename or "").suffix.lower() not in ALLOWED:
        return jsonify({"error": "Supported formats: CSV, TXT, XLSX and PDF."}), 400

    try:
        return jsonify(analyse(read_file(upload)))
    except Exception as error:
        return jsonify({"error": str(error)}), 400


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "Maximum upload size is 10 MB."}), 413



@app.get("/sample_recruitment.csv")
def sample_recruitment():
    return send_from_directory(
        app.root_path,
        "sample_recruitment.csv",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
