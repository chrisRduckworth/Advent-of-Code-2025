import re

def part_1(ranges):
    ids = []
    for r in ranges:
        for x in range(r[0], r[1]+1):
            if re.search(r'^(\d+)\1$', str(x)):
                ids.append(x)

    return sum(ids)

def part_2(ranges):
    # almost exactly the same, only the regex is slightly different 
    ids = []
    for r in ranges:
        for x in range(r[0], r[1]+1):
            if re.search(r'^(\d+)\1+$', str(x)):
                ids.append(x)

    return sum(ids)

if __name__ == "__main__":
    with open("inputs/day_02.txt") as f:
        input = f.read()
        input = input.split(",")
        ranges = [[int(k) for k in i.split("-")] for i in input]

        print(part_1(ranges))
        print(part_2(ranges))
