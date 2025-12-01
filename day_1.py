def part_1(instructions):
    pos = 50
    count = 0
    for i in instructions:
        if i[0] == "R":
            pos = (pos + i[1]) % 100
        elif i[0] == "L":
            pos = (pos - i[1]) % 100

        if pos == 0:
            count +=1 
    return count

def part_2(instructions):
    pos = 50
    count = 0

    for i in instructions:
        clicks = 0

        if i[0] == "R":
            pos = pos + i[1]
        elif i[0] == "L":
            if pos == 0:
                # so that if we go L from 0, it doesn't immediately click once
                pos = 100
            pos = pos - i[1]

        if pos >= 100:
            clicks = pos // 100

        if pos <= 0:
            # pos - 1 because we want 0 and to be a click, 100 2 clicks, etc
            clicks = abs((pos-1)//100)

        count += clicks
        pos = pos % 100

    return count



if __name__ == "__main__":
    with open("inputs/day_01.txt") as f:
        input = f.readlines()
        instructions = [[l[0], int(l[1:])] for l in input]
        zeros = part_1(instructions)
        print(zeros, "< part 1")
        clicks = part_2(instructions)
        print(clicks, "< part 2")

