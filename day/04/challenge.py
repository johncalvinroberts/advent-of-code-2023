import re


def parse_card(card: str):
    id_chunk, numbers_chunk = card.split(":")
    card_id_match = re.search(r"\d+", id_chunk)
    card_id_group = card_id_match.group() if card_id_match else None
    if card_id_group is None:
        raise RuntimeError("card id not found")
    card_id = int(card_id_group)
    left, right = numbers_chunk.split("|")

    # Extract numbers from left and right parts
    left_numbers = [int(num) for num in re.findall(r"\d+", left)]
    right_numbers = [int(num) for num in re.findall(r"\d+", right)]

    return card_id, left_numbers, right_numbers


def process_card(card) -> tuple[int, int, int]:
    identity, numbers, winning_numbers = parse_card(card)
    if identity is None:
        raise RuntimeError("identity not defined")
    points = 0
    matches = 0
    for number in numbers:
        if number in winning_numbers:
            matches += 1
            points = 1 if points < 1 else points * 2
    return identity, points, matches


# 17803
def part1(input_str: str):
    cards = input_str.strip().split("\n")
    total = 0
    for card in cards:
        _, points, __ = process_card(card)
        total += points
    return total


# should use a stack, LIFO
def part2(input_str: str):
    cards = input_str.strip().split("\n")
    card_count = 0
    cache = {}
    stack = cards.copy()
    while len(stack) > 0:
        card = stack.pop(0)
        card_count += 1
        if card not in cache:
            cache[card] = process_card(card)
        identity, _, matches = cache[card]
        for i in range(matches):
            if cards[i + identity]:
                stack.insert(0, cards[i + identity])
    return card_count


if __name__ == "__main__":
    fixture = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    expected = 13
    result = part1(fixture)
    assert result == expected
    expected2 = 30
    result2 = part2(fixture)
    assert result2 == expected2
