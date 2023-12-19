import re
import math


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
    mappings = {
        match[0]: {"L": match[1], "R": match[2]}
        for match in (re.findall(r"\b\w+\b", row) for row in rows)
    }
    starting_keys = [key for key in mappings if key.endswith("A")]

    def iterative_dfs(start_node):
        steps = 0
        node = start_node
        direction_index = 0

        while not node.endswith("Z"):
            # using modulo lets us cycle through directives infinitely
            next_direction = directives[direction_index % len(directives)]
            node = mappings[node][next_direction]
            direction_index += 1
            steps += 1

        return steps

    return math.lcm(*(iterative_dfs(node) for node in starting_keys))


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
