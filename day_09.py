def part_1(coords):
    max_area = 0
    for x_1, y_1 in coords:
        for x_2, y_2 in coords:
            d_x = abs(x_1 - x_2) + 1
            d_y = abs(y_1 - y_2) + 1
            area = d_x * d_y
            if area > max_area:
                max_area = area
    return max_area

# The following is a brute force solution using brute force
# It is very slow (22 seconds). After quite a long time 
# working on a different approach, I decided I just wanted 
# to finish the problem. I plan to revisit it.

# I'm pretty sure what I came up with should work:
#   For each rectangle created from two points,
#   check if the is a corner inside (excluding corners
#   and sometimes when it's on the edge). If there is,
#   The rectangle is invalid because a corner splits
#   it into an interior part and exterior

def part_2(coords):
    # Brute force using flood fill 

    # However just doing the naiive implementation goes OOM
    # as it tries to create 10,000,000,000 elements

    # So we compress the grid to only include the relevant
    # coordinates - each corner's x and y, as well as 
    # +/- 1 on each of those (so the surrounding square)
    
    # This is to make the flood fill easier and fix
    # problems which made sense at the time but now
    # I can't remember them

    # NB this is not particularly optimised because why
    # bother - it's a hacky brute force and saving a 
    # few seconds doesn't make it a nice solution

    # Start by finding unique coordinates
    x_coords = set() 
    y_coords = set()
    for x, y in coords:
        for i in range(-1, 2):
            x_coords.add(x + i)
            y_coords.add(y + i)

    # Now create the sorted list of coordinates for x and y
    x_coords = list(x_coords)
    y_coords = list(y_coords)
    x_coords.sort()
    y_coords.sort()
    # And we need to know where a value is in the array
    x_indices = {x: i for i, x in enumerate(x_coords)}
    y_indices = {y: i for i, y in enumerate(y_coords)}

    # Now create an unfilled grid
    tiles = [[0 for x in range(len(x_coords))] for y in range(len(y_coords))]


    # Now fill in the red tiles - along the lines
    for i, c_1 in enumerate((coords + [coords[0]])[:-1]):
        x_1, y_1 = c_1
        x_2, y_2 = (coords + [coords[0]])[i + 1]

        xi_start = x_indices[min(x_1, x_2)]
        xi_end = x_indices[max(x_1, x_2)] + 1
        yi_start = y_indices[min(y_1, y_2)]
        yi_end = y_indices[max(y_1, y_2)] + 1

        for x in range(xi_start, xi_end):
            for y in range(yi_start, yi_end):
                tiles[y][x] = 1

    
    # Now find an initial point to begin our floodfill
    initial_xi = 0 # always empty by definition
    initial_yi = y_indices[y_coords[1]] + 1 # always the middle
    # of a line (i.e. first intersection will be 1 then 0) by definition

    while True:
        tile = tiles[initial_yi][initial_xi]
        if tile == 1:
            # over the start line
            initial_xi += 1
            break
        initial_xi += 1


    # Now do a flood fill, beginning from initial point
    queue = [(initial_xi, initial_yi)]

    while len(queue) > 0:
        x, y = queue.pop()
        tiles[y][x] = 1

        dirs = ((1,0), (-1,0), (0,1), (0,-1))

        for dx, dy in dirs:
            if tiles[y + dy][x + dx] != 1:
                queue.append((x + dx, y + dy))

    # Finally, we can find the maximum area 
    # By checking whether the grid for a given
    # rectangle is all 1s (i.e. filled)
    max_area = 0

    for i, c_1 in enumerate(coords):
        x_1, y_1 = c_1
        x_1i = x_indices[x_1] # index of x_1 in x_coords
        y_1i = y_indices[y_1] # etc

        for c_2 in coords[i+1:]:
            x_2, y_2 = c_2
            area = (abs(x_1 - x_2) + 1) * (abs(y_1 - y_2) + 1)

            if area > max_area:
                x_2i = x_indices[x_2]
                y_2i = y_indices[y_2]


                min_xi, max_xi = (min(x_1i, x_2i), max(x_1i, x_2i))
                min_yi, max_yi = (min(y_1i, y_2i), max(y_1i, y_2i))

                # get the compressed grid representing the rectangle
                # created from c_1 and c_2
                rect = [l[min_xi: max_xi + 1] for l in tiles[min_yi:max_yi + 1]]

                # And just check it's all 1s
                if all([all(l) for l in rect]):
                    max_area = area

    return max_area

if __name__ == "__main__":
    with open("inputs/day_09.txt") as f:
        input = f.readlines()
        coords = [tuple(int(n) for n in l.split(",")) for l in input]
        print(part_1(coords))
        print(part_2(coords), "takes approx 22 seconds (Eugh)")
