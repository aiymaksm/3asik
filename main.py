import os
import csv
import json



class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print("File not found.")
            return False

    def create_output_folder(self, folder="output"):
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print("Output folder created.")
        else:
            print("Output folder already exists.")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                self.students = list(csv.DictReader(file))
            print(f"Data loaded successfully: {len(self.students)} students")
        except FileNotFoundError:
            print("File not found.")
        return self.students

    def preview(self, n=5):
        print("First 5 rows:")
        print("-" * 30)
        for student in self.students[:n]:
            print(
                f"{student['student_id']} | "
                f"{student['age']} | "
                f"{student['gender']} | "
                f"{student['country']} | "
                f"GPA: {student['GPA']}"
            )
        print("-" * 30)


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        print("Not implemented — use a child class")

    def print_results(self):
        for key, value in self.result.items():
            print(f"{key}: {value}")

    def __str__(self):
        return f"DataAnalyser: base class, {len(self.students)} students"


class TopStudentsAnalyser(DataAnalyser):
    def __init__(self, students):
        super().__init__(students)

    def analyse(self):
        sorted_students = sorted(
            self.students,
            key=lambda x: float(x["final_exam_score"]),
            reverse=True
        )

        top10 = sorted_students[:10]
        top_10_list = []

        for i, student in enumerate(top10, 1):
            top_10_list.append({
                "rank": i,
                "student_id": student["student_id"],
                "country": student["country"],
                "major": student["major"],
                "final_exam_score": float(student["final_exam_score"]),
                "GPA": float(student["GPA"])
            })

        self.result = {
            "analysis": "Top 10 Students by Exam Score",
            "total_students": len(self.students),
            "top_10": top_10_list
        }

        return self.result

    def print_results(self):
        print("=" * 40)
        print("TOP STUDENTS ANALYSIS REPORT")
        print("=" * 40)
        super().print_results()
        print("=" * 40)

    def __str__(self):
        return f"TopStudentsAnalyser: Top 10 Students, {len(self.students)} students"


class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        with open(self.output_path, "w", encoding="utf-8") as file:
            json.dump(self.result, file, indent=4)
        print(f"Result saved to {self.output_path}")



class Report:
    def __init__(self, analyser, saver):
        self.analyser = analyser
        self.saver = saver

    def generate(self):
        print("Generating report...")
        self.analyser.analyse()
        self.analyser.print_results()

        self.saver.result = self.analyser.result
        self.saver.save_json()

        print("Report complete.")


class SimpleCountAnalyser(DataAnalyser):
    def analyse(self):
        self.result = {
            "analysis": "Simple Count",
            "total_students": len(self.students)
        }
        return self.result

    def print_results(self):
        print("=" * 40)
        print("SIMPLE COUNT REPORT")
        print("=" * 40)
        super().print_results()
        print("=" * 40)

    def __str__(self):
        return f"SimpleCountAnalyser: {len(self.students)} students"



fm = FileManager("students.csv")

if not fm.check_file():
    print("Stopping program.")
    exit()

fm.create_output_folder()

dl = DataLoader("students.csv")
dl.load()
dl.preview()


analysers = [
    TopStudentsAnalyser(dl.students),
    SimpleCountAnalyser(dl.students[:10])
]

print("\nRunning all analysers:")
print("-" * 30)

for analyser in analysers:
    print(analyser)
    analyser.analyse()
    analyser.print_results()


main_analyser = TopStudentsAnalyser(dl.students)
main_analyser.analyse()

saver = ResultSaver(main_analyser.result, "output/result.json")
report = Report(main_analyser, saver)
report.generate()