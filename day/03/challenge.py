import re


def is_invalid_adjacent(row, prev_row, next_row, start, end):
    # Check left and right adjacent in the same row
    if (start > 0 and not (row[start - 1].isdigit() or row[start - 1] == ".")) or (
        end < len(row) and not (row[end].isdigit() or row[end] == ".")
    ):
        return True

    # Check adjacent characters in previous and next rows
    for adj_row in [prev_row, next_row]:
        if adj_row:
            for i in range(max(start - 1, 0), min(end + 1, len(adj_row))):
                if not (adj_row[i].isdigit() or adj_row[i] == "."):
                    return True

    return False


# Find all the part numbers. Part numbers are NUMBERS that are surrounded by a symbol.
# A char is a symbol if it's not a . or a number.
# Sum all the part numbers
def part1(input_str: str):
    schematic_rows = input_str.split("\n")
    part_numbers = []

    for index, row in enumerate(schematic_rows):
        prev_row = schematic_rows[index - 1] if index > 0 else None
        next_row = (
            schematic_rows[index + 1] if index < len(schematic_rows) - 1 else None
        )

        for match in re.finditer(r"\d+", row):
            number = int(match.group())
            start, end = match.span()

            if is_invalid_adjacent(row, prev_row, next_row, start, end):
                part_numbers.append(number)

    return sum(part_numbers)


def part2(input_str: str):
    pass


if __name__ == "__main__":
    fixture = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    result = part1(fixture)
    print(result)
    expected = 4361
    assert result == expected
    expected2 = 467835
    result2 = part2(fixture)
    assert result2 == expected2
