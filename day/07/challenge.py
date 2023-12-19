from functools import cmp_to_key


def compare_cards_recursively(hand1: str, hand2: str, cards_by_strength: str) -> int:
    h1 = cards_by_strength.index(hand1[0])
    h2 = cards_by_strength.index(hand2[0])
    # print(f"c1: {hand1}:{h1}, c2: {hand2}: {h2}")
    if h1 > h2:
        return -1
    if h1 < h2:
        return 1
    return compare_cards_recursively(hand1[1:], hand2[1:], cards_by_strength)


def compare_two_hands(
    hand1: list[str], hand2: list[str], use_jokers: bool, get_hand_score
):
    cards_by_strength = "AKQJT98765432"
    if use_jokers:
        cards_by_strength = "AKQT98765432J"
    # return 1 or -1, 1 if hand1 < hand2
    hand1_score = get_hand_score(hand1[0], use_jokers=use_jokers)
    hand2_score = get_hand_score(hand2[0], use_jokers=use_jokers)
    print(f"hand1: {hand1[0]}, score: {hand1_score}")
    print(f"hand2: {hand2[0]}, score: {hand2_score}")
    if hand1_score < hand2_score:
        return -1
    if hand1_score > hand2_score:
        return 1
    return compare_cards_recursively(hand1[0], hand2[0], cards_by_strength)


# sort the hands based on on rank
# add up the winnings
def part1(input_str: str):
    def get_hand_score(hand: str, use_jokers: bool = False):
        chars: dict[str, int] = {}
        for c in hand:
            chars[c] = chars.get(c, 0) + 1
        counts = chars.values()
        if 5 in counts:
            return 7
        if 4 in counts:
            return 6
        if 3 in counts:
            return 5 if 2 in counts else 4
        if list(counts).count(2) == 2:
            return 3
        if 2 in counts:
            return 2
        return 1

    def compare(hand1: list[str], hand2: list[str]):
        return compare_two_hands(
            hand1, hand2, use_jokers=False, get_hand_score=get_hand_score
        )

    rows = input_str.strip().split("\n")
    hands = list(map(lambda x: x.split(" "), rows))
    sorted_list = sorted(hands, key=cmp_to_key(compare))
    winnings = 0
    for idx, item in enumerate(sorted_list):
        winnings += int(item[1]) * (idx + 1)
    return winnings


def part2(input_str: str):
    def get_hand_score(hand: str, use_jokers: bool = False):
        chars: dict[str, int] = {}
        jokers = hand.count("J")
        for c in hand:
            if c != "J":
                chars[c] = chars.get(c, 0) + 1
        counts = sorted(chars.values(), reverse=True)
        if not counts:
            counts = [0]
        if counts[0] + jokers == 5:
            return 6
        if counts[0] + jokers == 4:
            return 5
        if counts[0] + jokers == 3 and counts[1] == 2:
            return 4
        if counts[0] + jokers == 3:
            return 3
        if counts[0] == 2 and (jokers or counts[1] == 2):
            return 2
        if counts[0] == 2 or jokers:
            return 1
        return 0

    def compare(hand1: list[str], hand2: list[str]):
        return compare_two_hands(
            hand1, hand2, use_jokers=True, get_hand_score=get_hand_score
        )

    rows = input_str.strip().split("\n")
    hands = list(map(lambda x: x.split(" "), rows))
    sorted_list = sorted(hands, key=cmp_to_key(compare))
    winnings = 0
    for idx, item in enumerate(sorted_list):
        winnings += int(item[1]) * (idx + 1)
    return winnings


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
    assert result == expected
    fixture2 = """
32T3K 100
22334 100
A23A4 100
23332 100
AA8AA 100
AAAAA 100"""
    result2 = part1(fixture2)
    expected2 = 2100
    assert result2 == expected2
    expected3 = 5905
    result3 = part2(fixture)
    print(result3)
    assert result3 == expected3

    fixture3 = """
JKKK2 10
QQQQ2 30"""
    expected4 = 70
    result4 = part2(fixture3)
    print(result4)
    assert result4 == expected4
