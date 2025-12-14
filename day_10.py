from z3 import Int, simplify, Solver, Sum, And, sat, Or

def push_button(state, button):
    output = [int(i) for i in state]
    for n in button:
        output[n] = (output[n] + 1) % 2 
    return tuple(bool(i) for i in output)

def part_1(lights, buttons):
    # Breadth first search

    total = 0
    for i in range(len(lights)):
        end = lights[i]
        button_array = buttons[i]
        states = {tuple(False for _ in range(len(end))): 0}
        j = 0
        while end not in states:
            to_add = []
            for state in {k:v for k, v in states.items() if v == j}:
                # for each state, push a button and see where it goes
                for button in button_array:
                    new_state = push_button(state, button)
                    if new_state not in states:
                        to_add.append([new_state, j + 1])
            for state, dist in to_add:
                states[state] = dist
            j += 1
        total += states[end]

    return total


def find_button_matrix(length, buttons_i):
    button_matrix = [[0 for _x in range(len(buttons_i))] for _y in range(length)]

    for x, button in enumerate(buttons_i):
        for b in button:
            button_matrix[b][x] = 1
            
    return button_matrix

def get_all_solutions(equation):
    # Shamelessly stolen from https://brandonrozek.com/blog/obtaining-multiple-solutions-z3/

    # find a solution
    # add it's negation as a constraint
    # (so we don't find the same solution again)
    # and repeat until there are no more solutions

    result = equation.check()
    solutions = []

    while result == sat:
        m = equation.model()
        solutions.append(m)
        solution_constraint = []
        for var in m:
            solution_constraint.append(var() != m[var])

        equation.add(Or(solution_constraint))
        result = equation.check()

    return solutions


def part_2(buttons, joltages):
    # I had three options:
    # 1: Guassian elimination
    #  - This is boring, I did it at uni
    #  and I have no interest in coding it
    # 2: Z3
    #  - Feels kind of cheaty, but at least
    #  I don't have to write option 1
    # 3: Simplex algorithm
    #  - People on reddit said this was an
    #  option, but I honestly can't see how
    #  you use it here - it's not an optimization
    #  problem

    # So I just used Z3 - at least I learnt something new

    total_presses = 0
    
    for i in range(len(joltages)):
        joltages_i = joltages[i]
        buttons_i = buttons[i]
        num_buttons = len(buttons_i)
        num_joltages = len(joltages_i)

        # create a matrix where i-th column is i-th button
        button_matrix = find_button_matrix(num_joltages, buttons_i)

        X = [Int('x%s' % i) for i in range(num_buttons)]

        s = Solver()

        # all button presses must be geq 0
        s.add(And([x >= 0 for x in X]))

        # create linear constraints from matrix
        for y, joltage in enumerate(joltages_i):
            # matrix multiplication to create equations
            linear_eq = Sum([button_matrix[y][x] * X[x] for x in range(num_buttons)])
            s.add(simplify(linear_eq == joltage))
        
        # now solve
        solutions = get_all_solutions(s)

        presses = [m.eval(Sum(X)).as_long() for m in solutions]
        total_presses += min(presses)


    return total_presses

if __name__ == "__main__":
    with open("inputs/day_10.txt") as f:
        input = [l[:-1] for l in f.readlines()]
        lights = [tuple(i == "#" for i in l.split(" ")[0][1:-1]) for l in input]
        buttons = [[[int(n) for n in s[1:-1].split(",")] for s in l.split(" ")[1:-1]] for l in input]
        joltages = [tuple(int(n) for n in l.split(" ")[-1][1:-1].split(",")) for l in input]
        print(part_1(lights, buttons))
        print(part_2(buttons, joltages))
