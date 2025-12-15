from functools import cache

def part_1(links):
    # Very simple DFS

    paths = 0
    queue = ["you"]
    
    while len(queue) > 0:
        link = queue.pop()
        if link == "out":
            paths += 1
        else:
            connected = links[link]
            queue.extend(connected)
    return paths

def part_2(links):
    # recursion with memoization,
    # keeping track of whether we've hit 
    # dac and fft

    @cache
    def count_paths(link, hit_dac, hit_fft):
        if link == "out":
            if hit_dac and hit_fft:
                return 1
            
            return 0

        paths = 0
        for l in links[link]:
            if link == "dac":
                paths += count_paths(l, True, hit_fft)
            elif link == "fft":
                paths += count_paths(l, hit_dac, True)
            else:
                paths += count_paths(l, hit_dac, hit_fft)

        return paths

    total_paths = count_paths("svr", False, False)

    return total_paths

if __name__ == "__main__":
    with open("inputs/day_11.txt") as f:
        input = [l[:-1] for l in f.readlines()]
        links = {l[:3]: l[5:].split(" ") for l in input}
        print(part_1(links))
        print(part_2(links))
