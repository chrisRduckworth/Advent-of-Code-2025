from functools import cache

def part_1(input):
    start_location = (0, input[0].index("S")) # (y, x)
    splitters = set()
    # create set of ^ locations
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if char == "^":
                splitters.add((y,x))
    
    hit_splitters = set() # for splitters hit by beams
    checked = set() # for beams added to queue not technically needed,
    # but makes it faster
    queue = [start_location]

    # take a beam, go down until it hits a splitter, then
    # add the beams split off to the queue
    # plus some checking for if we've hit them before/added
    # the beams before
    while len(queue) > 0:
        # go breadth first, it doesn't make much difference here
        y, x = queue.pop(0)
        dy = 1

        while y + dy < len(input):
            # follow the beam vertically downwards
            if (y + dy, x) in splitters:
                # we hit a splitter
                if (y + dy, x) not in hit_splitters:
                    # it hasn't been checked
                    # so add the child beams to the queue
                    # unless we've already added them (to be faster)
                    if (y + dy + 1, x - 1) not in checked:
                        queue.append((y + dy + 1, x - 1))
                        checked.add((y + dy + 1, x - 1))
                    if (y + dy + 1, x + 1) not in checked:
                        queue.append((y + dy + 1, x + 1))
                        checked.add((y + dy + 1, x + 1))
                    hit_splitters.add((y + dy, x))
                # the beam stops travelling once it hits a splitter
                break
            # we haven't hit a splitter, so move further down
            dy += 1
    return len(hit_splitters)


def part_2(input):
    start_location = (0, input[0].index("S")) # (y, x)
    splitters = set()

    # create set of ^ locations
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if char == "^":
                splitters.add((y,x))

    # recursively check left and right beams from splits
    # use memoization because if you hit the same splitter
    # from two directions, you get the same number of timelines
    # from that splitter

    @cache
    def count_timelines(beam):
        beam_y, beam_x = beam
        dy = 1
        # same as part 1, just have the beam go down until
        # it hits a splitter
        while beam_y + dy < len(input):
            if (beam_y + dy, beam_x) in splitters:
                # hit a splitter
                # run on left and right beams
                left_timelines = count_timelines((beam_y + dy + 1, beam_x - 1))
                right_timelines = count_timelines((beam_y + dy + 1, beam_x + 1))
                return left_timelines + right_timelines
            dy += 1
        
        # if we got here, then there are no more splitters,
        # i.e. we have hit the bottom row
        return 1

    return count_timelines(start_location)



if __name__ == "__main__":
    with open("inputs/day_07.txt") as f:
        input = f.readlines()
        print(part_1(input), "< part 1")
        print(part_2(input), "< part 2")

