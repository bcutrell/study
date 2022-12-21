
def main():
    #
    # day 1
    #
    with open('data/day_1.txt', 'r') as file:
        # Read all the lines in the file
        lines = file.readlines()

    # Iterate over the lines
    total = []
    calories = 0
    for line in lines:
        if line == "\n":
            total.append(calories)
            calories = 0
        else:
            calories += float(line.strip())

    print("Day 1", max(total))

    #
    # day 2
    #
    with open('data/day_2.txt', 'r') as file:
        # Read all the lines in the file
        lines = file.readlines()

    # A = Rock,1
    # B = Paper,2
    # C = Scissors,3
    #
    # X = Rock
    # Y = Paper
    # Z = Scissors
    #
    # win = 6
    # lose = 0
    # draw = 3

    score = 0
    for line in lines:
        line = line.strip()

        if line == "\n":
            continue

        opponent, you = line.split(" ")

        if you == "X":
            score += 1
        elif you == "Y":
            score += 2
        elif you == "Z":
            score += 3

        if opponent == "A":
            if you == "X":
                score += 3
            elif you == "Y":
                score += 6
            elif you == "Z":
                score += 0
        elif opponent == "B":
            if you == "X":
                score += 0
            elif you == "Y":
                score += 3
            elif you == "Z":
                score += 6
        elif opponent == "C":
            if you == "X":
                score += 6
            elif you == "Y":
                score += 0
            elif you == "Z":
                score += 3

    print("Day 2", score)

if __name__ == "__main__":
    main()
