def part1(input_str: str) -> int:
    rows = input_str.split("\n")
    calibration_vals: list[int] = []
    for row in rows:
        first = find_first_digit(row, detect_strings=False)
        last = find_first_digit(row, reverse=True, detect_strings=False)
        combined_digit = f"{first}{last}"
        calibration_vals.append(int(combined_digit))
    return sum(calibration_vals)


def part2(input_str: str):
    rows = input_str.split("\n")
    calibration_vals: list[int] = []
    for row in rows:
        first = find_first_digit(row, detect_strings=True)
        last = find_first_digit(row, reverse=True, detect_strings=True)
        combined_digit = f"{first}{last}"
        calibration_vals.append(int(combined_digit))
    return sum(calibration_vals)


def find_first_digit(row: str, reverse: bool = False, detect_strings=False) -> int:
    numbers = [
        ("one", 1),
        ("two", 2),
        ("three", 3),
        ("four", 4),
        ("five", 5),
        ("six", 6),
        ("seven", 7),
        ("eight", 8),
        ("nine", 9),
    ]
    if reverse:
        numbers = [(word[::-1], digit) for word, digit in numbers]
        row = row[::-1]
    for ind, char in enumerate(row):
        if char.isdigit():
            return int(char)
        if detect_strings:
            for word, digit in numbers:
                if row.startswith(word, ind):
                    return digit
    # fallback
    return 0


if __name__ == "__main__":
    fixture = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
    expected = 142
    result = part1(fixture)
    print(result)
    assert result == expected
    fixture2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    expected2 = 281
    result2 = part2(fixture2)
    print(result2)
    assert result2 == expected2
