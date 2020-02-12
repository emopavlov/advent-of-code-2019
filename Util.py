# Utility functions


def read_input(file, separator="\n"):
    rd = open("input/" + file, "r")

    out = []
    while True:
        line = rd.readline()
        if not line:
            break
        for elem in line.strip().split(separator):
            out.append(elem)

    rd.close()
    return out
