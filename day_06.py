from math import prod

def part_1(numbers, operators):
    results = []
    for i in range(0, len(numbers[0])):
        nums = [l[i] for l in numbers]
        operator = operators[i]
        if operator == "+":
            results.append(sum(nums))
        else:
            results.append(prod(nums))

    return sum(results)

def part_2(input):
    # to get the column of numbers, find the start index of the column using
    # the index of the operator

    operators = input[-1]
    numbers = input[:-1]

    numbers = [l + " " for l in numbers] # to pad final entry
    operator_indices = [i for i, o in enumerate(operators) if o in {"*", "+"} ]

    results = []

    # column by column, find the horizontal numbers, then use those
    # to find the vertical numbers
    
    # "right-to-left" is a red herring and doesn't matter because
    # addition and multiplication are commutative
    for index, operator_index in enumerate(operator_indices):
        operator = operators[operator_index]
        # the numbers horizontally
        if index == len(operator_indices) - 1:
            # final column
            numbers_string = [l[operator_index:-1] for l in numbers]
        else:
            numbers_string = [l[operator_index:operator_indices[index+1] - 1] for l in numbers]

        vertical_numbers = []
        for i in range(len(numbers_string[0])):
            # create the vertical number
            number_a = [s[i] for s in numbers_string if s[i] != " "]
            number = int("".join(number_a))
            vertical_numbers.append(number)

        # do the calculation
        if operator == "+":
            results.append(sum(vertical_numbers))
        else:
            results.append(prod(vertical_numbers))


    return sum(results)

if __name__ == "__main__":
    with open("inputs/day_06.txt") as f:
        input = [l[:-1] for l in f.readlines()]
        operators = [o for o in input[-1].split(" ") if len(o) > 0]
        numbers = [[int(n) for n in l.split(" ") if len(n) > 0] for l in input[:-1]]
        
        print(part_1(numbers, operators), "< part 1")
        print(part_2(input), "< part 2")
