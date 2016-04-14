# Sort this array by the length of the string, then alphabetical
# order (case-insensitive).  For example, a correctly sorted list
# might be:
#     a
#     D
#     z
#     vb
#     afd
def comparator(s1, s2):
    diff = len(s2) - len(s1)
    if diff > 0:
        return -1
    elif diff < 0:
        return 1
    else:
        return cmp(s1.lower(), s2.lower())


def sorted_data(data):
    data.sort(cmp=comparator)
    return data


def main():
    data = ["Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipisicing",
            "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore",
            "et"]
    for s in sorted_data(data):
        print s

if __name__ == "__main__":
    main()
