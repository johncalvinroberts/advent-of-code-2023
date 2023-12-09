import re


def parse_numbers(line: str):
    return [int(num) for num in re.findall(r"\d+", line)]


def group_in_threes(lst: list[int]):
    three = [lst[i : i + 3] for i in range(0, len(lst), 3)]
    return (three[0], three[1], three[2])


def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]


def parse_maps(chunks):
    maps = []
    curr_map: list[tuple[int, ...]] = []
    for d in chunks:
        if d == "":
            continue
        if ":" in d:
            maps += [curr_map]
            curr_map = []
        else:
            curr_map += [tuple(int(x) for x in d.split(" "))]

    maps += [curr_map]
    return maps


def apply_maps(maps, seed):
    pre_map = seed
    for m in maps:
        for ds, ss, rl in m:
            if ss <= pre_map < ss + rl:
                pre_map = ds + (pre_map - ss)
                break
    return pre_map


# The input consists of two parts: a list of seeds, followed by a series of mapping configs
# The mapping configs are each itself a series of ranges.
# [destination start value], [source start value], [range]
# Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
# Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
# Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
# Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
def part1(input_str: str):
    input_str = input_str.strip()
    chunks = input_str.split("\n")
    seeds = parse_numbers(chunks[0])
    maps = parse_maps(chunks[3:])
    cache: dict[int, int] = {}
    locs = {}
    for s in seeds:
        if s in cache:
            result = cache[s]
            locs[result] = s
        else:
            result = apply_maps(maps, s)
            cache[s] = result
            locs[result] = s
    min_loc = min(locs.keys())
    return min_loc


def part2_og(input_str: str):
    input_str = input_str.strip()
    chunks = input_str.split("\n")
    raw_seeds = parse_numbers(chunks[0])
    raw_maps = parse_maps(chunks[3:])

    for raw_map in raw_maps:
        print(len(raw_map))


# NOT MY SOLUTION
# JFC THIS PROBLEM IS KINDA HARD
def part2(text):
    seeds = []
    seed_maps = []

    for line in text.split("\n"):
        if len(line) != 0:
            if re.match("^seeds:.+", line):
                for seed_pair in re.findall(r"(\d+) (\d+)", line):
                    seeds.append(
                        {
                            "start": int(seed_pair[0]),
                            "end": int(seed_pair[0]) + int(seed_pair[1]) - 1,
                        }
                    )
            elif re.match(".*map:", line):
                seed_maps.append([])
            else:
                decoded_map = re.match(r"(\d+) (\d+) (\d+)", line)
                if decoded_map:
                    seed_maps[-1].append(
                        {
                            "difference": int(decoded_map.group(2))
                            - int(decoded_map.group(1)),
                            "source_start": int(decoded_map.group(2)),
                            "source_end": int(decoded_map.group(2))
                            + int(decoded_map.group(3))
                            - 1,
                        }
                    )
    print(seed_maps)

    def sortBySource(map):
        return map["source_start"]

    for i, seed_map in enumerate(seed_maps):
        seed_map.sort(key=sortBySource)

    these_ranges = seeds

    for seed_map in seed_maps:
        next_ranges = []
        for seed in these_ranges:
            current_seed_start = seed["start"]
            for single_seed_map in seed_map:
                possible_start = max(
                    single_seed_map["source_start"], current_seed_start
                )

                if possible_start > seed["end"]:
                    break

                possible_end = min(single_seed_map["source_end"], seed["end"])

                if possible_end >= possible_start:
                    if current_seed_start < possible_start:
                        next_ranges.append(
                            {"start": current_seed_start, "end": possible_start - 1}
                        )
                    next_ranges.append(
                        {
                            "start": possible_start - single_seed_map["difference"],
                            "end": possible_end - single_seed_map["difference"],
                        }
                    )
                    current_seed_start = possible_end + 1

            if current_seed_start < seed["end"]:
                next_ranges.append({"start": current_seed_start, "end": seed["end"]})

        these_ranges = next_ranges.copy()

    def sortByStart(seed):
        return seed["start"]

    next_ranges.sort(key=sortByStart)
    return next_ranges[0]["start"]


if __name__ == "__main__":
    fixture = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
    result = part1(fixture)
    expected = 35
    assert result == expected
    result2 = part2(fixture)
    result22 = part2_og(fixture)
    print(result2)
    expected2 = 46
    assert result2 == expected2
