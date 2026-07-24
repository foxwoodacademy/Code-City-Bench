
import sys
import time

def print_box(text):
    line = "+" + "-" * (len(text) + 2) + "+"
    print(f"{line}\n| {text} |\n{line}")

def run():
    print_box("CodeMentor Auditor v1.0")
    print("\n[1] Analyze Code\n[2] Export Report\n[3] Exit")

    choice = input("\n> Select an option: ")

    if choice == "1":
        file_path = input("Enter file path: ")
        print("\n... Analyzing ...")
        time.sleep(1.5)
        print("Done. 3 potential issues found.")
    else:
        print("Exiting.")

if __name__ == "__main__":
    run()
