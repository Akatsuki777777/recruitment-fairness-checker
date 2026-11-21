import csv
from collections import defaultdict
from pathlib import Path

INPUT = Path("sample_recruitment.csv")
OUTPUT = Path("fairness_report.csv")

REQUIRED = {"candidate_id", "group", "qualified", "selected"}
SMALL_SAMPLE_SIZE = 30
SCREENING_THRESHOLD = 0.80


def load_data():
    groups = defaultdict(lambda: {
        "applicants": 0,
        "selected": 0,
        "qualified": 0,
        "qualified_selected": 0
    })

    seen_ids = set()

    with INPUT.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain: {sorted(REQUIRED)}")

        for line, row in enumerate(reader, start=2):
            candidate_id = (row["candidate_id"] or "").strip()
            group = (row["group"] or "").strip()

            if not candidate_id or not group:
                raise ValueError(f"Missing candidate ID or group on line {line}")

            if candidate_id in seen_ids:
                raise ValueError(f"Duplicate candidate ID: {candidate_id}")

            seen_ids.add(candidate_id)

            try:
                qualified = int(row["qualified"])
                selected = int(row["selected"])
            except (ValueError, TypeError):
                raise ValueError(f"Invalid numeric value on line {line}")

            if qualified not in (0, 1) or selected not in (0, 1):
                raise ValueError(f"Values must be 0 or 1 on line {line}")

            if selected and not qualified:
                raise ValueError(
                    f"Selected candidate is marked unqualified on line {line}"
                )

            data = groups[group]
            data["applicants"] += 1
            data["selected"] += selected
            data["qualified"] += qualified
            data["qualified_selected"] += selected

    if not groups:
        raise ValueError("The dataset contains no candidate records.")

    return groups


def compare_rates(rates):
    if len(rates) < 2:
        return None, None, None, "Insufficient groups for comparison"

    highest_group = max(rates, key=rates.get)
    lowest_group = min(rates, key=rates.get)

    highest = rates[highest_group]
    lowest = rates[lowest_group]

    if highest == 0:
        return lowest_group, highest_group, None, "No selections recorded"

    ratio = lowest / highest

    if ratio < SCREENING_THRESHOLD:
        status = "Below optional 0.80 screening threshold"
    else:
        status = "At or above optional 0.80 screening threshold"

    return lowest_group, highest_group, ratio, status


def main():
    groups = load_data()
    report = []
    all_rates = {}
    qualified_rates = {}

    print("\nRECRUITMENT FAIRNESS CHECKER — VERSION 3")
    print("=" * 50)

    for group, data in sorted(groups.items()):
        applicants = data["applicants"]
        selected = data["selected"]
        qualified = data["qualified"]
        qualified_selected = data["qualified_selected"]

        all_rate = selected / applicants
        qualified_rate = (
            qualified_selected / qualified if qualified else None
        )

        all_rates[group] = all_rate

        if qualified_rate is not None:
            qualified_rates[group] = qualified_rate

        warning = (
            "Small sample: interpret cautiously"
            if applicants < SMALL_SAMPLE_SIZE else ""
        )

        print(f"\n{group}")
        print(f"Applicants: {applicants}")
        print(f"Selected: {selected}")
        print(f"All-applicant selection rate: {all_rate:.1%}")
        print(f"Qualified applicants: {qualified}")

        if qualified_rate is None:
            print("Qualified selection rate: N/A")
        else:
            print(f"Qualified selection rate: {qualified_rate:.1%}")

        if warning:
            print(f"WARNING: {warning}")

        report.append({
            "record_type": "group",
            "group": group,
            "applicants": applicants,
            "selected": selected,
            "all_applicant_selection_rate": f"{all_rate:.4f}",
            "qualified_applicants": qualified,
            "qualified_selected": qualified_selected,
            "qualified_selection_rate": (
                f"{qualified_rate:.4f}" if qualified_rate is not None else "N/A"
            ),
            "comparison_low_group": "",
            "comparison_high_group": "",
            "selection_rate_ratio": "",
            "screening_interpretation": "",
            "sample_warning": warning
        })

    print("\nCOMPARISON RESULTS")
    print("-" * 50)

    for label, rates in [
        ("All applicants", all_rates),
        ("Qualified applicants", qualified_rates)
    ]:
        low_group, high_group, ratio, status = compare_rates(rates)

        print(f"\n{label}:")
        if ratio is None:
            print(status)
        else:
            print(f"Lowest-rate group: {low_group}")
            print(f"Highest-rate group: {high_group}")
            print(f"Lowest-to-highest ratio: {ratio:.2f}")
            print(status)

        if ratio is not None:
            report.append({
                "record_type": "comparison",
                "group": label,
                "applicants": "",
                "selected": "",
                "all_applicant_selection_rate": "",
                "qualified_applicants": "",
                "qualified_selected": "",
                "qualified_selection_rate": "",
                "comparison_low_group": low_group,
                "comparison_high_group": high_group,
                "selection_rate_ratio": f"{ratio:.4f}",
                "screening_interpretation": status,
                "sample_warning": ""
            })

    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=report[0].keys())
        writer.writeheader()
        writer.writerows(report)

    print(f"\nReport saved: {OUTPUT}")

    print("\nIMPORTANT LIMITATIONS")
    print("- Small samples make rates unstable.")
    print("- The 0.80 threshold is only a screening convention.")
    print("- A ratio does not establish discrimination or fairness.")
    print("- Job relevance, data quality and other factors need review.")
    print("- This tool does not establish legal compliance.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"\nERROR: {error}")
        raise SystemExit(1)
