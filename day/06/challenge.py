import re
from functools import reduce


def parse_numbers(line: str):
    return [int(num) for num in re.findall(r"\d+", line)]


# Determine the number of ways you could beat the record in each race
# Multiply the number of ways to beat the record and return that value
def part1(input_str: str):
    input_str = input_str.strip()
    rows = input_str.split("\n")
    races = parse_numbers(rows[0])
    records = parse_numbers(rows[1])
    ways: list[int] = []
    for i, race_duration in enumerate(races):
        ways.append(0)
        record = records[i]
        for r in range(1, race_duration):
            dur = race_duration - r
            dist = r * dur
            if dist > record:
                ways[i] = ways[i] + 1
    return reduce(lambda x, y: x * y, ways)


# Much longer race :|
def part2(input_str: str):
    rows = input_str.strip().split("\n")
    duration = int("".join(re.findall(r"\d", rows[0])))
    record = int("".join(re.findall(r"\d", rows[1])))
    ways = 0
    for r in range(1, duration):
        dur = duration - r
        dist = r * dur
        if dist > record:
            ways += 1
    return ways


if __name__ == "__main__":
    fixture = """
Time:      7  15   30
Distance:  9  40  200
"""
    expected = 288
    result = part1(fixture)
    assert result == expected
    expected2 = 71503
    result2 = part2(fixture)
    assert result2 == expected2
