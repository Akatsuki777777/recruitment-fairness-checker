# Recruitment Fairness Checker

An independent Python and Flask project exploring recruitment outcome disparities through group-level selection-rate analysis.

Built as a practical learning project in AI governance, algorithmic fairness, responsible evaluation and human oversight.

**Live application:** https://recruitment-fairness-checker.onrender.com

**Source code:** https://github.com/Akatsuki777777/recruitment-fairness-checker

## 1. Project Purpose

Recruitment decisions can affect people's access to employment opportunities. When selection processes use automated systems or structured decision-making, differences in outcomes across groups deserve careful examination.

This project provides a basic tool for comparing recruitment outcomes across groups. It calculates selection rates, compares the lowest and highest rates, and flags results that may warrant further investigation.

The project is intended for educational exploration. It does not establish whether a recruitment system is fair, discriminatory or legally compliant.

## 2. Features

- Upload recruitment datasets in CSV, TXT, XLSX and experimental text-based PDF formats.
- Validate required columns and candidate records.
- Check unique candidate identifiers and binary values.
- Reject selections of candidates marked as unqualified.
- Calculate applicant and selection totals for each group.
- Calculate selection rates for all applicants and qualified applicants.
- Compare the lowest and highest group selection rates.
- Flag ratios below the optional 0.80 screening threshold.
- Identify groups with fewer than 30 applicants.
- Download a CSV analysis report containing calculated results.
- Download a prepared synthetic sample dataset.
- Run automated tests for important validation cases.

## 3. How the Analysis Works

The application calculates two types of selection rates.

**All-applicant selection rate**

Number of selected applicants divided by the total number of applicants in a group.

**Qualified-applicant selection rate**

Number of selected qualified applicants divided by the total number of qualified applicants in a group.

It then calculates the lowest-to-highest selection-rate ratio:

Ratio = Lowest group selection rate / Highest group selection rate

A ratio below 0.80 is flagged as an optional screening signal.

The 0.80 threshold is not a universal legal standard and should not be interpreted as proof of discrimination.

## 4. Technology

- Python 3
- Flask — web application and API
- OpenPyXL — Excel workbook reading
- pypdf — text extraction from PDFs
- CSV and Python standard library — data processing
- unittest — automated testing
- Gunicorn — production application server
- HTML, CSS and JavaScript — user interface

## 5. Supported Input Format

Each dataset must contain these four columns:

| Column | Description |
|---|---|
| candidate_id | Unique candidate identifier |
| group | Group used for comparison |
| qualified | 1 if qualified, otherwise 0 |
| selected | 1 if selected, otherwise 0 |

Additional requirements:

- Candidate IDs must be unique and non-empty.
- Group names must be present.
- qualified and selected must contain only 0 or 1.
- An unqualified candidate cannot be marked as selected.
- Maximum upload size: 10 MB.

**File format notes**

- CSV: Comma-separated data.
- TXT: Delimited text using comma, semicolon or tab.
- XLSX: Data must be in the first worksheet.
- PDF: Experimental support for PDFs containing extractable, delimited table text. Scanned PDFs and complex visual tables are not supported.

## 6. Example Results

The included synthetic dataset contains 100 fictional candidate records.

| Measure | Group A | Group B |
|---|---:|---:|
| Applicants | 50 | 50 |
| Selected | 18 | 12 |
| All-applicant selection rate | 36% | 24% |
| Qualified applicants | 40 | 40 |
| Qualified selection rate | 45% | 30% |

The lowest-to-highest ratio is approximately **0.67** for both comparisons.

This is a screening signal that may justify further investigation. It is not evidence by itself of discrimination or unfair treatment.

## 7. Running the Application Locally

Clone the repository:

```bash
git clone https://github.com/Akatsuki777777/recruitment-fairness-checker.git
cd recruitment-fairness-checker
```

Create and activate a virtual environment if desired, then install dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask application:

```bash
python app.py
```

Open the local address shown by Flask in your browser. By default, this application uses:

`http://127.0.0.1:5000`

## 8. Running Automated Tests

Run:

```bash
python -m unittest -v
```

The current test suite contains six tests covering:

1. Valid input data
2. Empty datasets
3. Missing required columns
4. Duplicate candidate IDs
5. Invalid binary values
6. Selection of an unqualified candidate

**Latest recorded result:** Six tests passed.

## 9. Project Structure

| File | Purpose |
|---|---|
| app.py | Flask application, upload handling and analysis API |
| fairness_checker.py | Python command-line analysis program |
| index.html | Web application interface |
| test_fairness_checker.py | Automated tests |
| sample_recruitment.csv | Synthetic sample dataset |
| fairness_report.csv | Example command-line analysis output |
| requirements.txt | Python dependencies |

## 10. Limitations and Responsible Use

- The supplied data is synthetic and does not represent real recruitment outcomes.
- Small sample sizes can produce unstable selection rates.
- The 0.80 threshold is an optional screening convention, not a universal legal test.
- Selection-rate differences alone cannot establish discrimination, causation or fairness.
- The analysis does not account for job relevance, data quality, confounding variables or the full recruitment process.
- Qualified-applicant comparisons do not establish that qualification criteria are themselves fair.
- PDF support is experimental and depends on extractable, correctly structured text.
- Uploaded data should not contain personal or confidential candidate information.
- The tool should not be used as the sole basis for real recruitment decisions.

Meaningful fairness assessments require contextual investigation, appropriate expertise, and human oversight.

## 11. Project Status

**Status:** Independent learning prototype.

The project demonstrates practical work in:

- Data validation and processing
- Group-level outcome analysis
- Selection-rate comparisons
- Basic fairness screening
- Automated software testing
- Building and deploying a small web application

It is not a production recruitment auditing system or a validated AI fairness assessment framework.

## Author

**Sahe Alam Khan**

- GitHub: https://github.com/Akatsuki777777
- LinkedIn: https://www.linkedin.com/in/aalam-khan-819310401
- Portfolio: https://aalam-khan-portfolio.netlify.app/

---

Created as an independent educational project exploring practical AI governance, recruitment fairness and responsible evaluation.
