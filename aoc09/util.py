from typing import List


def read_input(file: str, separator="\n") -> List[str]:
    with open("../input/" + file, "r") as rd:
        out = []
        for line in rd:
            for elem in line.strip().split(separator):
                out.append(elem)

    return out
