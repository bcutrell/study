
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

    print(max(total))

if __name__ == "__main__":
    main()
