# Utility functions


def read_input(file, separator="\n"):
    with open("../input/" + file, "r") as rd:
        out = []
        for line in rd:
            for elem in line.strip().split(separator):
                out.append(elem)

    return out
