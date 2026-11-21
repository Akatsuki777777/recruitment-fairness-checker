import csv
import subprocess
import tempfile
import unittest
import shutil
from pathlib import Path

SCRIPT = Path(__file__).with_name("fairness_checker.py").resolve()

class FairnessCheckerTests(unittest.TestCase):

    def run_checker(self, headers, rows):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            shutil.copy(SCRIPT, folder / "fairness_checker.py")

            with (folder / "sample_recruitment.csv").open(
                "w", newline="", encoding="utf-8"
            ) as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(rows)

            return subprocess.run(
                ["python", "fairness_checker.py"],
                cwd=folder,
                capture_output=True,
                text=True
            )

    def test_valid_data(self):
        result = self.run_checker(
            ["candidate_id", "group", "qualified", "selected"],
            [
                ["1", "A", 1, 1],
                ["2", "A", 1, 0],
                ["3", "B", 1, 0],
                ["4", "B", 1, 0],
            ]
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Lowest-to-highest ratio: 0.00", result.stdout)

    def test_duplicate_ids(self):
        result = self.run_checker(
            ["candidate_id", "group", "qualified", "selected"],
            [["1", "A", 1, 1], ["1", "B", 1, 0]]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Duplicate candidate ID", result.stdout)

    def test_invalid_binary_value(self):
        result = self.run_checker(
            ["candidate_id", "group", "qualified", "selected"],
            [["1", "A", 2, 0]]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Values must be 0 or 1", result.stdout)

    def test_unqualified_selection(self):
        result = self.run_checker(
            ["candidate_id", "group", "qualified", "selected"],
            [["1", "A", 0, 1]]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Selected candidate is marked unqualified", result.stdout)

    def test_missing_column(self):
        result = self.run_checker(
            ["candidate_id", "group", "selected"],
            [["1", "A", 1]]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("CSV must contain", result.stdout)

    def test_empty_dataset(self):
        result = self.run_checker(
            ["candidate_id", "group", "qualified", "selected"],
            []
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no candidate records", result.stdout)

if __name__ == "__main__":
    unittest.main(verbosity=2)
