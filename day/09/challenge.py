def signed_difference(a, b):
    return (b - a) if a <= b else (a - b) * -1


def get_extrapolated_value(
    nums: list[int], memo: list[list[int]], reverse: bool
) -> int:
    diffs = [nums[i] - nums[i - 1] for i in range(1, len(nums))]
    memo.append(diffs)
    done = all(item == 0 for item in diffs)
    if not done:
        return get_extrapolated_value(diffs, memo, reverse=reverse)
    snapshots = list(reversed(memo))
    for index, snapshot in enumerate(snapshots):
        if index == len(snapshots) - 1:
            return snapshot[-1] if not reverse else snapshot[0]
        previous_snapshot = snapshots[index + 1]
        if not reverse:
            previous_snapshot_next_val = snapshot[-1] + previous_snapshot[-1]
            previous_snapshot.append(previous_snapshot_next_val)
            continue
        else:
            previous_snapshot_prev_val = signed_difference(
                snapshot[0], previous_snapshot[0]
            )
            previous_snapshot.insert(0, previous_snapshot_prev_val)
            continue
    return 0


# extrapolate the next value in each row by iterating the difference down to all 0s
# return the sum of the extrapolated values of all rows
def part1(input_str: str):
    rows = input_str.strip().split("\n")
    extrapolated_values: list[int] = []
    for row in rows:
        nums = list(map(lambda x: int(x), row.split(" ")))
        extrapolated_values.append(get_extrapolated_value(nums, [nums], reverse=False))
    return sum(extrapolated_values)


def part2(input_str: str):
    rows = input_str.strip().split("\n")
    extrapolated_values: list[int] = []
    for row in rows:
        nums = list(map(lambda x: int(x), row.split(" ")))
        extrapolated_values.append(get_extrapolated_value(nums, [nums], reverse=True))
    return sum(extrapolated_values)


if __name__ == "__main__":
    fixture = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    expected = 114
    result = part1(fixture)
    assert result == expected
    expected2 = 2
    result2 = part2(fixture)
    assert result2 == expected2
