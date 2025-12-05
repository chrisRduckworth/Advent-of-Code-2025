def part_1(ranges, ingredients):
    fresh = 0
    for ingredient in ingredients:
        for lower, upper in ranges:
            if lower <= ingredient and ingredient <= upper:
                fresh += 1
                break
    return fresh

def part_2(ranges):
    # go through the sorted ranges, combine two if the end of 
    # one is >= the start of the next
    # repeat until nothing changes, then you have the list of
    # reduced intervals

    ranges.sort(key=lambda x: x[0])
    new_ranges = ranges

    prev_length = len(new_ranges)
    new_length = -1 # temp value

    while prev_length > new_length: # i.e. as long as two intervals have reduced to one
        to_skip = False
        temp_new_range = []
        
        for i, interval in enumerate(new_ranges[:-1]):
            # check if end >= start_next
            # if YES:
            # combine them into a single interval, and skip the next
            # iteration
            # if NO:
            # add the interval

            if to_skip:
                # skipping if previously merged
                to_skip = False
                continue

            start, end = interval
            start_next, end_next = new_ranges[i + 1]
            to_add = []

            if end >= start_next:
                # merge 
                to_skip = True
                to_add = [start, max(end, end_next)]
            else:
                # no merge
                to_add = [start, end]

            temp_new_range.append(to_add)

        if not to_skip:
            # for the final interval, add it if it 
            # hasn't been merged
            to_add = new_ranges[-1]
            temp_new_range.append(to_add)


        # update lengths & range array for next iteration
        prev_length = len(new_ranges)
        new_ranges = temp_new_range
        new_length = len(new_ranges)

    # calculate lengths of intervals
    lengths = [end - start + 1 for start, end in new_ranges]
    return sum(lengths)

if __name__ == "__main__":
    with open("inputs/day_05.txt") as f:
        input = f.read()

        ranges, ingredients = input.split("\n\n")
        ranges = [[int(x) for x in r.split("-")] for r in ranges.splitlines()]
        ingredients = [int(x) for x in ingredients.splitlines()]

        print(part_1(ranges, ingredients), "< part 1")
        print(part_2(ranges), "< part 2")
