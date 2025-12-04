def part_1(banks):
    joltages = []
    for bank in banks:
        digit_1 = max(bank[:-1])
        i_1 = bank.index(digit_1)
        digit_2 = max(bank[i_1 + 1:])
        joltage = digit_1 * 10 + digit_2
        joltages.append(joltage)
    return sum(joltages)

def part_2(banks):
    # the value of a digit is the maximum possible of the values in the range it can be
    # eg 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 
    # first digit must have index in [0,3], call it i_0
    # then second digit must have index in [i_0, 4], call it i_1
    # etc

    # so the position of the k-th (k in [0,11]) digit is in [i_{k-1}, len(bank) - 12 + k]
    # and it's value is the maximum of the values in that interval

    joltages = []
    length = len(banks[0])
    for bank in banks:
        joltage = ""
        lower_limit = 0 # lowest possible index for digit
        for k in range(12):
            upper_limit = length - 12 + k # highest possible index for digit
            poss_values = bank[lower_limit: upper_limit + 1]
            digit = max(poss_values)
            i_k = poss_values.index(digit) + lower_limit # index of digit

            lower_limit = i_k + 1
            joltage = joltage + str(digit)

            # it is possible to decrease run time once the remaining length 
            # of the bank is the same as what's needed for joltage
            # but it's only relatively small, given the longest steps
            # (max and .index) are working over an array of size 1

        joltages.append(int(joltage))
    return sum(joltages)

with open("day_03.txt") as f:
    input = f.readlines()
    banks = [[int(c) for c in l.strip()] for l in input] 
    print(part_1(banks), "< part 1")
    print(part_2(banks), "< part 2")