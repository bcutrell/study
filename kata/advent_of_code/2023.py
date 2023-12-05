import argparse
import typing

def day1():
    """
        $ Part 1:  53334
        $ Part 2:  52834
    """
    data = []

    # START: Part 1
    total = 0
    with open('day1_input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            nums = []
            for char in line:
                if char.isdigit():
                    nums.append(char)

            combined_num = int(nums[0] + nums[-1])
            total += combined_num
            data.append(line) # add line to data
    print("Part 1: ", total)
    # END: Part 1

    num_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    word_to_num_str = { "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
                        "six": "6", "seven": "7", "eight": "8", "nine": "9" }

    updated_total = 0
    for line in data:
        # find the first number in the string, it can be in int or word form
        first_num = ""
        index = 0
        for char in line:
            if char.isdigit():
                first_num += char
            else:
                for word in num_words:
                    if word == line[index:index+len(word)]:
                        first_num += word_to_num_str[word]
                        break
            index += 1

            if first_num != "":
                break

        second_num = ""
        i = 0
        for char in line[::-1]:
            if char.isdigit():
                second_num = char
                break
            else:
                for word in num_words:
                    if i == 0:
                        comp = line[len(line)-len(word):]
                    else:
                        comp = line[len(line)-i-len(word):-i]
                    if word == comp:
                        second_num = word_to_num_str[word]
                        break
            i += 1
            if second_num != "":
                break

        if first_num == "" or second_num == "":
            print(f"first_num={first_num}, second_num={second_num} line={line}")
            raise Exception("first_num or second_num is empty")
        else:
            pass

        combined_num = int(first_num + second_num)
        updated_total += combined_num
    print("Part 2: ", updated_total)


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

def main():
    day1()
    day2()


if __name__ == "__main__":
    main()