
def test(number):
    ints = [(number//(10**i)) % 10 for i in range(5, -1, -1)]
    increasing = True
    same_neighbours = False

    for i in range(0, 5):
        increasing = increasing and ints[i] <= ints[i+1]

    for i in range(0, 5):
        same_neighbours = same_neighbours or ints[i] == ints[i + 1]

    return increasing and same_neighbours


possible_passwords = 0
for n in range(178416, 676461):
    if test(n):
        possible_passwords += 1


print("Part One", possible_passwords)


def test2(number):
    ints = [(number // (10 ** i)) % 10 for i in range(5, -1, -1)]
    increasing = True
    same_neighbours = []

    for i in range(0, 5):
        increasing = increasing and ints[i] <= ints[i + 1]

    last = -1
    for i in range(0, 6):
        if last != ints[i]:
            last = ints[i]
            same_neighbours.append(1)
        else:
            same_neighbours[-1] += 1

    return increasing and 2 in same_neighbours


possible_passwords = 0
for n in range(178416, 676461):
    if test2(n):
        possible_passwords += 1


print("Part Two", possible_passwords)
