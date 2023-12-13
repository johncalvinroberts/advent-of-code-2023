from functools import cmp_to_key

cards_by_strength = "AKQJT98765432"


# 7 score types.
# 5 duplicates -> 7
# 4 duplicates -> 6
# Full house: 3 duplicates + 2 duplicates (e.g., 23332) -> 5
# 3 duplicates -> 4
# 2 duplicates * 2 (e.g., 22334) -> 3
# 1 duplicates -> 2
# No duplicates -> 1
def get_hand_score(hand: str):
    quints = 0
    quads = 0
    triples = 0
    doubles = 0
    chars: dict[str, int] = {}
    for c in hand:
        if c in chars:
            chars[c] += 1
        else:
            chars[c] = 1
    for key in chars:
        count = chars[key]
        if count == 5:
            quints = 1
            break
        if count == 4:
            quads = 1
            break
        if count == 3:
            triples = 1
        if count == 2:
            doubles += 1
    score = 1
    if quints > 0:
        score = 7
    if quads > 0:
        score = 6
    if triples > 0 and doubles > 0:
        score = 5
    if triples > 0 and doubles < 1:
        score = 4
    if triples < 1 and doubles > 1:
        score = 3
    if triples < 1 and doubles > 0:
        score = 2
    return score


def compare_cards_recursively(hand1: str, hand2: str) -> int:
    h1 = cards_by_strength.index(hand1[0])
    h2 = cards_by_strength.index(hand2[0])
    print(f"c1: {hand1}:{h1}, c2: {hand2}: {h2}")
    if h1 > h2:
        return -1
    if h1 < h2:
        return 1
    return compare_cards_recursively(hand1[1:], hand2[1:])


def compare_two_hands(hand1: list[str], hand2: list[str]):
    # return 1 or -1, 1 if hand1 < hand2
    hand1_score = get_hand_score(hand1[0])
    hand2_score = get_hand_score(hand2[0])
    print(f"hand1: {hand1[0]}, score: {hand1_score}")
    print(f"hand2: {hand2[0]}, score: {hand2_score}")
    if hand1_score < hand2_score:
        return -1
    if hand1_score > hand2_score:
        return 1
    return compare_cards_recursively(hand1[0], hand2[0])


# sort the hands based on on rank
# add up the winnings
def part1(input_str: str):
    rows = input_str.strip().split("\n")
    hands = list(map(lambda x: x.split(" "), rows))
    sorted_list = sorted(hands, key=cmp_to_key(compare_two_hands))
    winnings = 0
    for idx, item in enumerate(sorted_list):
        winnings += int(item[1]) * (idx + 1)
    return winnings


def part2(input_str: str):
    pass


# 32T3K
# KTJJT
# KK677
# QQQJA
# T55J5
if __name__ == "__main__":
    fixture = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
    expected = 6440
    result = part1(fixture)
    print(result)
    assert result == expected
    # fixture2, expected2 = ("", "")# Put simple fixture here
    # result2 = part2(fixture2)
    # assert result2 == expected2
