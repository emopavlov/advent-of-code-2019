from typing import List


def read_input(file: str, separator: str = '\n', should_strip: bool = True, folder: str = "../input/") -> List[str]:
    with open(folder + file, "r") as rd:
        out = []
        for line in rd:
            if should_strip:
                line = line.strip()
            for elem in line.split(separator):
                if elem != '':
                    out.append(elem)

    return out
