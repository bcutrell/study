import argparse
import re
import typing

#
# Constants
#
WORD_TO_NUM_STR = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

#
# Helpers
#
def read_file(filename: str) -> typing.List[str]:
    data = []
    with open(filename, "r") as file:
        for line in file:
            data.append(line.strip())
    return data

def find_first_occurance(line, words):
    pattern = '|'.join(map(re.escape, words))
    match = re.search(pattern, line)
    return match.group(0) if match else None

def find_matches(line, words):
    pattern = '|'.join(map(re.escape, words))
    matches = re.findall(pattern, line)
    return matches

#
# Days
#
def day1():
    """
        $ Part 1:  53334
        $ Part 2:  52834
    """
    data = read_file('day1_input.txt')

    # Part 1
    part_1 = 0
    for line in data:
        nums = []
        for char in line:
            if char.isdigit():
                nums.append(char)

        combined_num = int(nums[0] + nums[-1])
        part_1 += combined_num
    print("Part 1: ", part_1)

    # Part 2
    part_2 = 0
    for line in data:
        match_nums = find_matches(line, list(WORD_TO_NUM_STR.keys()) + list(WORD_TO_NUM_STR.values()))

        first_match = match_nums[0]
        if first_match in WORD_TO_NUM_STR:
            first_match = WORD_TO_NUM_STR[first_match]
        last_match = match_nums[-1]
        if last_match in WORD_TO_NUM_STR:
            last_match = WORD_TO_NUM_STR[last_match]

        combined_num = int(first_match + last_match)
        part_2 += combined_num
    print("Part 2: ", part_2)

    return (part_1, part_2)


def day2():
    """
        $ Part 1: 2505
        $ Part 2:  70265
    """
    game_log = {}
    # Part 1:
    # 12 red cubes, 13 green cubes, and 14 blue cubes
    with open('day2_input.txt', 'r') as f:
        game_log = {}
        invalid_game_ids = set()

        for line in f:
            line = line.strip()
            game_id, games = line.split(":")

            game_id = int(game_id.split(" ")[-1])
            game_log[game_id] = []

            for game in games.split(";"):
                color_counts = {
                    "red": 0,
                    "green": 0,
                    "blue": 0
                }
                for g in game.split(","):
                    count, color = g.strip().split(" ")
                    color_counts[color] += int(count)

                game_log[game_id].append(color_counts)

                for color in color_counts:
                    if color == "red" and color_counts[color] > 12:
                        invalid_game_ids.add(game_id)

                    if color == "green" and color_counts[color] > 13:
                        invalid_game_ids.add(game_id)

                    if color == "blue" and color_counts[color] > 14:
                        invalid_game_ids.add(game_id)

        total = 0
        for id in game_log:
            if id in invalid_game_ids:
                continue
            else:
                total += id
        print("Part 1: ", total)

        # Part 2:
        powers = []
        for key, games in game_log.items():
            # find maximum count for each color
            max_red = 0
            max_green = 0
            max_blue = 0
            for game in games:
                if game["red"] > max_red:
                    max_red = game["red"]
                if game["green"] > max_green:
                    max_green = game["green"]
                if game["blue"] > max_blue:
                    max_blue = game["blue"]

            power = max_red*max_green*max_blue
            powers.append(power)

        print("Part 2: ", sum(powers))

def get_adjacent_points(data, i, j):
    points = {}

    # check all adjacent points in grid
    # check left
    if j-1 >= 0:
        points['left_point'] = data[i][j-1]

    # check right
    if j+1 < len(data[i]):
        points['right_point'] = data[i][j+1]

    # check up
    if i-1 >= 0:
        points['up_point'] = data[i-1][j]

    # check down
    if i+1 < len(data):
        points['down_point'] = data[i+1][j]

    # check diagonals
    # check upper left
    if i-1 >= 0 and j-1 >= 0:
        points['upper_left_point'] = data[i-1][j-1]

    # check upper right
    if i-1 >= 0 and j+1 < len(data[i]):
        points['upper_right_point'] = data[i-1][j+1]

    # check lower left
    if i+1 < len(data) and j-1 >= 0:
        points['lower_left_point'] = data[i+1][j-1]

    # check lower right
    if i+1 < len(data) and j+1 < len(data[i]):
        points['lower_right_point'] = data[i+1][j+1]

    return points

def get_adjacent_indexes(data, i, j):
    indexes = {}

    # check all adjacent points in grid
    # check left
    if j-1 >= 0:
        indexes['left_point'] = (i, j-1)

    # check right
    if j+1 < len(data[i]):
        indexes['right_point'] = (i, j+1)

    # check up
    if i-1 >= 0:
        indexes['up_point'] = (i-1, j)

    # check down
    if i+1 < len(data):
        indexes['down_point'] = (i+1, j)

    # check diagonals
    # check upper left
    if i-1 >= 0 and j-1 >= 0:
        indexes['upper_left_point'] = (i-1, j-1)

    # check upper right
    if i-1 >= 0 and j+1 < len(data[i]):
        indexes['upper_right_point'] = (i-1, j+1)

    # check lower left
    if i+1 < len(data) and j-1 >= 0:
        indexes['lower_left_point'] = (i+1, j-1)

    # check lower right
    if i+1 < len(data) and j+1 < len(data[i]):
        indexes['lower_right_point'] = (i+1, j+1)

    return indexes

def day3():
    """
        $ Part 1:  557705
        $ Part 2:  84266818
    """
    # Part 1:
    data = []
    with open('day3_input.txt', 'r') as f:
        data = []
        for line in f:
            line = line.strip()
            data.append(line)

    symbols = ['*', '-', '@', '#', '+', '&', '=', '%', '/', '$']
    numbers_adjacent_to_symbols = []
    is_digit = False
    is_valid = False
    digit = ""
    for i in range(len(data)):
        for j in range(len(data[i])):
            point = data[i][j]
            left_point = None
            right_point = None
            up_point = None
            down_point = None
            upper_left_point = None
            upper_right_point = None
            lower_left_point = None
            lower_right_point = None

            if point.isdigit():
                is_digit = True
                digit += point

                # check all adjacent points in grid
                points = get_adjacent_points(data, i, j)

                # check if any adjacent points are symbols
                for _point in points.values():
                    if _point in symbols:
                        is_valid = True

            else:
                if is_digit and digit != "" and is_valid:
                    numbers_adjacent_to_symbols.append(digit)

                is_digit = False
                digit = ""
                is_valid = False

    print("Part 1: ", sum([int(num) for num in numbers_adjacent_to_symbols]))

    # Part 2:
    index_to_digit = {}
    digit = ""
    is_digit = False
    indexes = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            point = data[i][j]
            if point.isdigit():
                indexes.append((i, j))
                is_digit = True
                digit += point
            else:
                if is_digit and digit != "":
                    for index in indexes:
                        index_to_digit[index] = digit
                is_digit = False
                digit = ""
                indexes = []

    numbers_adjacent_to_star = []
    result = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            point = data[i][j]
            if point == "*":
                indexes = get_adjacent_indexes(data, i, j)
                nums = []
                for idx in indexes.values():
                    if idx in index_to_digit:
                        num = index_to_digit[idx]
                        if num not in nums:
                            nums.append(num)
                print(nums)
                if len(nums) == 2:
                    result += (int(nums[0]) * int(nums[1]))
                nums = []

    print("Part 2: ", result)

def day4():
    """
        $ Part 1:  25174
        $ Part 2:  6420979
    """
    with open("test.txt", "r") as file:
        data = file.read()

    cards = [line.split(":")[1].strip().split("|") for line in data.splitlines()]
    sum = 0
    copy_count = 0
    copies = [0] * len(cards)
    for i, card in enumerate(cards):
        print(f"card={card}, i={i}, copies={copies}, sum={sum}, copy_count={copy_count}, repeat_count={1 + copies[i]}")
        winners = set(map(int, card[0].split()))
        match_count = len([int(num) for num in card[1].split() if int(num) in winners])

        repeat_count = 1 + copies[i]
        copy_count += repeat_count

        for j in range(i + 1, i + match_count + 1):
            if j < len(copies):
                copies[j] += repeat_count

        sum += 2 ** (match_count - 1) if match_count > 0 else 0

    print(f"First part results: {sum}")
    print(f"Second part results: {copy_count}\n")

#
# Main
#
def main():
    day1()
    day2()
    day3()
    day4()

#
# Tests
#
def test_day1():
    assert day1() == (53334, 52834)

def test_day2():
    pass

def test_day3():
    pass

def test_day4():
    pass

if __name__ == "__main__":
    main()