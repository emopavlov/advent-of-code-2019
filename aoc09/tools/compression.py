def sequence_compare(source, target, pos):
    target_len = len(target)
    for (i, s) in enumerate(source):
        if pos + i >= target_len or target[pos + i] != s:
            return False
    return True


def replace_all(sequence, subsequence, replacement):
    def intersperse(lst, item):
        result = [item] * (len(lst) * 2 - 1)
        result[0::2] = lst
        return result

    i = 0
    last_index = len(sequence) - len(subsequence)
    matches = []
    while i <= last_index:
        if sequence_compare(subsequence, sequence, i):
            matches.append(i)
            i += len(subsequence)
        else:
            i += 1

    if len(matches) == 0:
        return [sequence]
    else:
        last_match = 0
        result = []
        for k in matches:
            result.append(sequence[last_match:k])
            last_match = k + len(subsequence)
        result.append(sequence[last_match:len(sequence)])

        return list(filter(lambda x: x, intersperse(result, [replacement])))


def replace(sequences, subsequence, replacement):
    result = []
    for r in sequences:
        the_split = replace_all(r, subsequence, replacement)
        if len(result) > 0 and len(the_split) > 0:
            if result[-1] == []:
                result.pop(-1)
            if the_split[0] == []:
                the_split.pop(0)
        result.extend(the_split)
    return result


def pick_subsequence(sequence, length):
    return sequence[0:length]


def compress(sequences, dict_size, word_size, dict):
    def seeds():
        for seed in (x for x in sequences if x[0][0] != ':'):
            for i in range(1, min(word_size, len(seed)) + 1):
                yield pick_subsequence(seed, i)

    for ss in seeds():
        result = replace(sequences, ss, ':' + str(dict_size))
        if len(result) <= word_size:
            if all(x[0][0] == ':' for x in result):
                print("JACKPOT!")
                print(dict + [ss])
                print(result)
            elif dict_size > 1:
                compress(result, dict_size - 1, word_size, dict + [ss])
