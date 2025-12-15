def part_1(presents, regions):
    # looking at the input, you can see that either:
    # the presents easily fit (without any packing, just assuming each takes up 3x3) or
    # the presents are nowhere near fitting

    # so we can simply just calculate whether the total area of presents
    # is <= area of the region

    present_areas = ["".join(p).count("#") for p in presents]

    total = 0
    for h, w, count in regions:
        area = h * w
        present_area = sum(p * present_areas[i] for i, p in enumerate(count))

        if present_area <= area:
            total += 1

    return total

if __name__ == "__main__":
    with open("inputs/day_12.txt") as f:
        input = f.read()
        presents = [p[3:].split("\n") for p in input.split("\n\n")[:-1]]
        regions = []
        for r in input.split("\n\n")[-1].splitlines():
            area, counts = r.split(": ")
            h, w = [int(n) for n in area.split("x")]
            counts = [int(n) for n in counts.split(" ")]
            regions.append((h,w, counts))

        print(part_1(presents, regions))
