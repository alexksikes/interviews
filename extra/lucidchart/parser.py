# Write a small, reasonably efficient class that takes strings
# as input, and calls a callback method whenever a newline ("\n")
# is reached, passing in the previous line's text. The class
# should discard old data when possible to save memory.
#
# Hint: This should not take more than about 15-50 lines of code.
class LineParser(object):
    def __init__(self, callback):
        self.callback = callback
        self._buffer = ""

    def read(self, data):
        for c in data:
            if c == '\n':
                self.callback(self._buffer)
                self._buffer = ""
            else:
                self._buffer += c


def main():
    def print_line(line):
        print line.replace("\n", " ")
    parser = LineParser(print_line)
    parser.read("This is t")
    parser.read("he first l")
    parser.read("ine.\nAnd this is the second.\n")
    parser.read("And this is the third.\nAnd the")
    parser.read(" fourth.\n")


if __name__ == "__main__":
    main()
