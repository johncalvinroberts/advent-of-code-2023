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


def compose_string_chunk_with_numbers_in_tact(row: str | None, idx: int):
    if row is None:
        return "..."

    def find_sequence_boundaries(s, index, forward=True):
        while index >= 0 and index < len(s) and s[index].isdigit():
            index += 1 if forward else -1
        return index + (0 if forward else 1)

    start_idx = find_sequence_boundaries(row, idx - 1, forward=False)
    end_idx = find_sequence_boundaries(row, idx + 1, forward=True)

    chunk = row[start_idx:end_idx]

    # Ensuring that the chunk is at least 3 characters long
    if len(chunk) < 3:
        chunk = chunk.rjust(3, ".")[:3]

    return chunk


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


# Any "*" that touches two numbers is a gear ratio, get the value by multiplying the two numbers it touches
# return the sum of all gear ratios
def part2(input_str: str):
    schematic_rows = input_str.split("\n")
    gear_ratios: list[int] = []
    for index, row in enumerate(schematic_rows):
        prev_row = schematic_rows[index - 1] if index > 0 else None
        next_row = (
            schematic_rows[index + 1] if index < len(schematic_rows) - 1 else None
        )
        for c_idx, char in enumerate(row):
            if char == "*":
                curr_string = compose_string_chunk_with_numbers_in_tact(row, c_idx)
                prev_string = compose_string_chunk_with_numbers_in_tact(prev_row, c_idx)
                next_string = compose_string_chunk_with_numbers_in_tact(next_row, c_idx)
                numbers = []
                for span in [prev_string, curr_string, next_string]:
                    susbtring_numbers = [int(num) for num in re.findall(r"\d+", span)]
                    numbers.extend(susbtring_numbers)
                if len(numbers) >= 2:
                    gear_ratios.append(numbers[0] * numbers[1])
    return sum(gear_ratios)


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
    expected = 4361
    assert result == expected
    expected2 = 467835
    result2 = part2(fixture)
    print(result2)
    assert result2 == expected2
