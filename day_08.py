import math
from itertools import chain
from collections import defaultdict

def part_1(boxes, pairs=1000):
    shortest_connections = [(math.inf, (0,0,0), (0,0,0)) for _ in range (pairs)]

    for i, box_1 in enumerate(boxes):
        x_1, y_1, z_1 = box_1
        for box_2 in boxes[i+1:]:
            x_2, y_2, z_2 = box_2
            dist = ((x_1 - x_2) ** 2 ) + ((y_1 - y_2) ** 2) + ((z_1 - z_2) ** 2)
            if dist < shortest_connections[-1][0]:
                # distance is in shortest
                for j, connection in enumerate(shortest_connections):
                    dist_j = connection[0]
                    if dist < dist_j:
                        new_connection = (dist, box_1, box_2)
                        shortest_connections.insert(j,new_connection)
                        shortest_connections.pop()
                        break


    # think about this as a graph
    nodes = list([(c[1], c[2]) for c in shortest_connections])
    nodes = {n: set() for n in chain.from_iterable(nodes)}

    for connection in shortest_connections:
        box_1, box_2 = connection[1:]
        nodes[box_1].add(box_2)
        nodes[box_2].add(box_1)


    checked = set()
    circuits = []

    for node, adj in nodes.items():
        # dfs to find connection components
        if node not in checked:
            circuit = set()
            circuit.add(node)
            checked.add(node)
            queue = [n for n in adj]
            while len(queue) > 0:
                n_1 = queue.pop()
                adj_1 = nodes[n_1]
                if n_1 not in checked:
                    circuit.add(n_1)
                    checked.add(n_1)
                    for n_2 in adj_1:
                        queue.append(n_2)
            circuits.append(circuit)

    lengths = [len(c) for c in circuits]
    lengths.sort(reverse=True)

    return math.prod(lengths[:3])

def part_2(boxes):
    ### PRIMS ALGORITHM - we need a minimal spanning tree
    # cp-algorithms.com/graph/mst_prim.html
    # that website is bloody brilliant

    # essentially, choose an initial vertex. Then find
    # the nearest vertex. Now repeat for the nearest vertex
    # to one of the two vertices. etc

    # we use a slightly modified version because the graph is
    # complete (and therefore dense)

    # this matches the input, because for a box to be connected,
    # it's first edge to be connected will be the lowest value edge
    # which is the same as the one the algorithm gives


    connections = defaultdict(dict)
    # connections is of the form:
    # { box: {connected_box: distance}}

    for box_1 in boxes:
        x_1, y_1, z_1 = box_1
        for box_2 in boxes:
            x_2, y_2, z_2 = box_2
            dist = ((x_1 - x_2) ** 2 ) + ((y_1 - y_2) ** 2) + ((z_1 - z_2) ** 2)
            connections[box_1][box_2] = dist


    # stores whether a box has been added to the spanning tree
    selected = {b: False for b in boxes}

    # min_e stores the distance from each vertex to the nearest 
    # already selected vertex
    # and is of the form {box: {weight: n, to: another_box}}
    min_e = {b: {"weight": math.inf, "to": -1} for b in boxes}
    min_e[boxes[0]]["weight"] = 0 # for the first iteration

    final_edge = []

    for _ in range(len(boxes)):
        selected_box = -1 # placeholder

        # this finds the unselected box with minimum distance
        # to an already connected box
        for box_i in boxes: 
            if not selected[box_i] and ( # iterate over unselected boxes
                    selected_box == -1 or # for first iteration
                    min_e[box_i]["weight"] < min_e[selected_box]["weight"] 
                    # i.e. box_i is closer than the currently selected box
                    ):
                selected_box = box_i

        selected[selected_box] = True

        # this is just for calculating the final answer
        final_edge = [selected_box, min_e[selected_box]["to"]]

        # now update the distance from each unselected box
        # to the nearest connected box
        for box_i in boxes:
            # only the connections for selected_box need to be
            # updated
            if connections[selected_box][box_i] < min_e[box_i]["weight"]:
                min_e[box_i] = {"weight": connections[selected_box][box_i], "to": selected_box}


    return final_edge[0][0] * final_edge[1][0]

if __name__ == "__main__":
    with open("inputs/day_08.txt") as f:
        input = f.readlines()
        boxes = [tuple(int(n) for n in l.split(",")) for l in input]
        print(part_1(boxes), "< part 1")
        print(part_2(boxes), "< part 2")
