# Recruitment Fairness Checker

A beginner-built Python tool for exploring selection-rate differences in
synthetic recruitment data. It is an independent learning project focused
on practical AI governance, algorithmic fairness and responsible evaluation.

## Project Overview

The checker analyses recruitment outcomes across groups and calculates:

- Number of applicants in each group
- Number and percentage selected
- Number of qualified applicants
- Selection rate among qualified applicants
- Lowest-to-highest selection-rate ratios
- Flags for ratios below an optional 0.80 screening threshold

It also generates a CSV report for further review.

## Why This Project Matters

Automated recruitment systems can affect access to employment.
Comparing selection outcomes can help identify patterns that deserve
closer investigation.

This tool demonstrates a basic, practical approach to examining
potential disparities. It does not determine whether an AI system
is fair, discriminatory or legally compliant.

## Technology

- Python 3
- CSV data processing
- Python standard library
- Unit testing with `unittest`

No third-party Python packages are required.

## Project Files

| File | Description |
|---|---|
| `fairness_checker.py` | Main Version 3 program |
| `sample_recruitment.csv` | Synthetic 100-record dataset |
| `fairness_report.csv` | Generated analysis report |
| `test_fairness_checker.py` | Automated test suite |
| `fairness_checker_v1.py` | Earlier development version |
| `fairness_checker_v2.py` | Earlier development version |

## Requirements

- Python 3.8 or later
- A terminal or command-line environment

## How to Run

Clone or download this repository, then open its directory.

Run the checker:

```bash
python fairness_checker.py
```

The program reads `sample_recruitment.csv` and creates or updates
`fairness_report.csv`.

## Run the Automated Tests

```bash
python -m unittest -v test_fairness_checker.py
```

The current test suite contains six tests covering:

1. Valid input data
2. Empty datasets
3. Missing required columns
4. Duplicate candidate IDs
5. Invalid binary values
6. Unqualified candidate selection

Latest recorded verification: **6 tests passed**.

## Input Data Format

The input CSV must contain these columns:

| Column | Meaning |
|---|---|
| `candidate_id` | Unique candidate identifier |
| `group` | Group used for comparison |
| `qualified` | 1 if qualified, otherwise 0 |
| `selected` | 1 if selected, otherwise 0 |

The binary fields must contain valid 0 or 1 values.

The supplied dataset is fictional and was created for demonstration
and testing. It does not contain real candidate information.

## Example Results

For the included 100-record synthetic dataset:

| Measure | Group A | Group B |
|---|---:|---:|
| Applicants | 50 | 50 |
| Selected | 18 | 12 |
| All-applicant selection rate | 36% | 24% |
| Qualified applicants | 40 | 40 |
| Qualified selection rate | 45% | 30% |

The lowest-to-highest selection-rate ratio is approximately **0.67**
for both comparisons.

This result is a reason to investigate further, not proof of
discrimination.

## Important Limitations

- The supplied dataset is synthetic and deliberately constructed.
- Small samples can produce unstable rates.
- The 0.80 threshold is an optional screening convention, not a
  universal legal standard.
- Selection-rate ratios alone cannot establish discrimination or fairness.
- Job relevance, data quality, qualifications and other contextual
  factors require examination.
- The tool does not test a real AI model or establish legal compliance.
- Results should be reviewed by appropriately qualified people before
  any organisational decision is made.

## Project Status

Version 3 — Early-stage independent learning prototype.

The project demonstrates basic data validation, group-level outcome
comparison, CSV reporting and automated testing. It is not a production
recruitment audit system.

## Author

**Sahe Alam Khan**

- GitHub: https://github.com/Akatsuki777777
- LinkedIn: https://www.linkedin.com/in/aalam-khan-819310401
- Portfolio: https://aalam-khan-portfolio.netlify.app/

---

Created as an independent educational project exploring practical
AI governance and recruitment fairness.
