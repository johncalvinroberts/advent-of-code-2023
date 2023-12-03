import re
from functools import reduce


def parse_game_info(game_str) -> tuple:
    # Regular expression to extract the game ID and the rounds
    match = re.match(r"Game (\d+): (.+)", game_str)
    if not match:
        raise Exception("invalid input")

    game_id = str(match.group(1))
    rounds_str = match.group(2)

    rounds = []
    for round_str in rounds_str.split(";"):
        # Extracting color and count pairs
        round_info = re.findall(r"(\d+) (\w+)", round_str)
        round_dict: dict[str, int] = {color: int(count) for count, color in round_info}
        rounds.append(round_dict)

    return (int(game_id), rounds)


# Determine which games would be possible with the following configuration:
# only 12 red cubes, 13 green cubes, and 14 blue cubes
# sum the ids of the possible games
def part1(input_str: str) -> int:
    config = {"red": 12, "green": 13, "blue": 14}
    valid_game_ids = []
    games = input_str.split("\n")
    for game in games:
        if len(game) < 1:
            continue
        game_id, rounds = parse_game_info(game)
        valid = True
        for round in rounds:
            for color, value in round.items():
                if config[color] < value:
                    valid = False
        if valid:
            valid_game_ids.append(game_id)
    return sum(valid_game_ids)


# find the number of cubes needed for each color, then multiply those, store that in "powers"
# then return the sum of powers
def part2(input_str: str):
    games = input_str.split("\n")
    sum_of_powers = 0
    for game in games:
        if len(game) < 1:
            continue
        min_counts = {"red": 0, "green": 0, "blue": 0}
        _, rounds = parse_game_info(game)
        for round in rounds:
            for color, count in round.items():
                min_counts[color] = max(count, min_counts[color])
        power = reduce(lambda x, y: x * y, min_counts.values(), 1)
        sum_of_powers += power

    return sum_of_powers


if __name__ == "__main__":
    fixture = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    expected = 8
    result = part1(fixture)
    assert result == expected
    expected2 = 2286
    result2 = part2(fixture)
    assert result2 == expected2
