def part_1(input):
    # pad input to make counting adjacents easier on edge
    padded_input = ["." + line + "." for line in input]
    padded_input.insert(0, "." * len(padded_input[0]))
    padded_input.append("." * len(padded_input[0]))

    valid = 0

    for y in range(1, len(padded_input)-1):
        line = padded_input[y]
        for x in range(1, len(line)-1):
            char = line[x]
            if char == "@": # check adjacent
                adjacent_rolls = 0
                for d_x in range(-1, 2):
                    for d_y in range(-1,2):
                        if padded_input[y + d_y][x + d_x] == "@": 
                            adjacent_rolls += 1

                adjacent_rolls -= 1 # because we included d_x = d_y = 0 i.e. the original @

                if adjacent_rolls < 4:
                    valid += 1

    return valid

def part_2(input):
    # same as part 1, except we keep track of which rolls to remove
    # and continue doing it until there are no more to remove
    padded_input = ["." + line + "." for line in input]
    padded_input.insert(0, "." * len(padded_input[0]))
    padded_input.append("." * len(padded_input[0]))
    padded_input = [list(l) for l in padded_input]

    valid = 0
    to_change = [None]

    while len(to_change) > 0:
        to_change = []
        for y in range(1, len(padded_input)-1):
            line = padded_input[y]
            for x in range(1, len(line)-1):
                char = line[x]
                if char == "@":
                    adjacent_rolls = 0
                    for d_x in range(-1, 2):
                        for d_y in range(-1,2):
                            if padded_input[y + d_y][x + d_x] == "@":
                                adjacent_rolls += 1 
                    adjacent_rolls -= 1

                    if adjacent_rolls < 4:
                        to_change.append((y, x))

        valid += len(to_change)
        for y, x in to_change:
            padded_input[y][x] = "."

    return valid

if __name__ == "__main__":
    with open("inputs/day_04.txt") as f:
        input = [l[:-1] for l in f.readlines()]
        print(part_1(input), "< part 1")
        print(part_2(input), "< part 2")
