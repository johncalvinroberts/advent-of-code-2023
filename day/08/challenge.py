import re


# Goal: find how many steps are required to reach ZZZ
def part1(input_str: str) -> int:
    chunks = input_str.strip().split("\n\n")
    directives = list(chunks[0])
    rows = chunks[1].split("\n")
    mappings: dict[str, tuple[str, str]] = {}
    for row in rows:
        matches = re.findall(r"\b\w+\b", row)
        mappings[matches[0]] = (matches[1], matches[2])
    key = "AAA"
    steps = 0
    while key != "ZZZ":
        for directive in directives:
            left, right = mappings[key]
            if directive == "L":
                key = left
            if directive == "R":
                key = right
            steps += 1
    return steps


def part2(input_str: str) -> int:
    chunks = input_str.strip().split("\n\n")
    directives = list(chunks[0])
    rows = chunks[1].split("\n")
    mappings: dict[str, tuple[str, str]] = {}
    starting_keys: list[str] = []
    for row in rows:
        matches = re.findall(r"\b\w+\b", row)
        key = matches[0]
        mappings[key] = (matches[1], matches[2])
        if key.endswith("A"):
            starting_keys.append(key)
    steps = 0

    condition = lambda x: x.endswith("Z")

    def shall_we_continue():
        # Some magical logic here
        # Return True to continue, False to stop
        if all(condition(item) for item in starting_keys):
            return False
        return True

    while shall_we_continue():
        for directive in directives:
            for idx, key in enumerate(starting_keys):
                left, right = mappings[key]
                if directive == "L":
                    key = left
                if directive == "R":
                    key = right
                starting_keys[idx] = key
            steps += 1

    return steps


if __name__ == "__main__":
    fixture1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
    result1 = part1(fixture1)
    expected1 = 2
    assert result1 == expected1
    fixture2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    expected2 = 6
    result2 = part1(fixture2)
    assert result2 == expected2
    fixture3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    expected3 = 6
    result3 = part2(fixture3)
    assert result3 == expected3
