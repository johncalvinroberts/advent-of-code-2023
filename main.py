import argparse
import requests
from utils.os import read_file, write_file, make_dir, import_module_from_file
import os
import subprocess
import sys


day_path = os.path.join(os.getcwd(), "day")


def run_all():
    print("Running all days! hohoho")
    for folder in sorted(os.listdir(day_path)):
        folder_path = os.path.join(day_path, folder)
        if os.path.isdir(folder_path) and folder.isdigit():
            run_day(int(folder))


def run_day(day: int):
    dirname = os.path.join(day_path, f"{day:02d}")
    input_file = f"{dirname}/input.txt"
    chlg_file = f"{dirname}/challenge.py"
    # Dynamically import the module
    chlg_module = import_module_from_file(chlg_file)
    input_raw = read_file(input_file)
    # Run part1 and part2
    print(f"🦌 Running day {day}")
    print("Part 1:", chlg_module.part1(input_raw))
    print("Part 2:", chlg_module.part2(input_raw))


def scaffold(day: int):
    cookie = read_file("cookie")
    url = f"https://adventofcode.com/2023/day/{day}/input"
    headers = {"cookie": f"session={cookie}"}

    response = requests.get(url, headers=headers)
    # This will raise an error for non-200 responses
    response.raise_for_status()

    data = response.content

    dirname = os.path.join(day_path, f"{day:02d}")
    input_file = f"{dirname}/input.txt"
    chlg_file = f"{dirname}/challenge.py"

    chlg_scaffold = """
def part1(input_str: str):
    pass


def part2(input_str: str):
    pass


if __name__ == "__main__":
    fixture, expected = ("", "")  # Put simple fixture here
    result = part1(fixture)
    assert result == expected
    # fixture2, expected2 = ("", "")# Put simple fixture here
    # result2 = part2(fixture2)
    # assert result2 == expected2
"""

    make_dir(dirname)
    write_file(input_file, data)
    write_file(chlg_file, chlg_scaffold)

    print("🌲🌲好了！Done! ❄️❄️❄️❄️")


def format_self():
    try:
        result = subprocess.run(
            ["black", "."], check=True, text=True, capture_output=True
        )
        print("Black formatting completed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error during Black formatting:", e.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Process some commands.")
    parser.add_argument(
        "--cmd",
        choices=["run", "scaffold"],
        required=False,
        default="run",
        help='Command to execute, can be "run" or "scaffold" or "format"',
    )
    parser.add_argument("--day", type=int, required=False, help="Day number")
    args = parser.parse_args()
    if args.cmd == "format":
        format_self()
    elif args.cmd == "run" and args.day is None:
        run_all()
    elif args.cmd == "run" and args.day is not None:
        run_day(args.day)
    elif args.cmd == "scaffold" and args.day is None:
        raise RuntimeError("Cannot scaffold if day is not provided")
    else:
        scaffold(args.day)


if __name__ == "__main__":
    main()
