import re


# Find all the part numbers. Part numbers are NUMBERS that are surrounded by a symbol.
# A char is a symbol if it's not a . or a number.
# Sum all the part numbers
def part1(input_str: str):
    schematic_rows = input_str.split("\n")
    part_numbers: list[int] = []
    for index, row in enumerate(schematic_rows):
        previous_row = schematic_rows[index - 1] if index > 0 else None
        next_row = (
            schematic_rows[index + 1] if index < len(schematic_rows) - 1 else None
        )
        numbers_with_index = []
        for match in re.finditer(r"\d+", row):
            number = int(match.group())
            start = match.start()
            end = match.end()
            numbers_with_index.append((start, end, number))
        for start, end, n in numbers_with_index:
            adjacents = []
            if start > 0:
                adjacents.append(row[start - 1])
            if end + 1 < len(row):
                adjacents.append(row[end])
            if previous_row:
                chunk_start = start - 1 if start > 0 else 0
                chunk_end = end + 1 if end + 1 < len(row) else end
                chunk = previous_row[chunk_start:chunk_end]
                adjacents.extend(chunk)
            if next_row:
                chunk_start = start - 1 if start > 0 else 0
                chunk_end = end + 1 if end + 1 < len(row) else end
                chunk = next_row[chunk_start:chunk_end]
                adjacents.extend(chunk)
            no_symbols = all(item.isdigit() or item == "." for item in adjacents)
            if not no_symbols:
                part_numbers.append(n)
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
