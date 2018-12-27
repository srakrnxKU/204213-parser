"""
Parser programme for Theory of Computation course,
Sirakorn Lamyai (5910500023)
Department of Computer Engineering, Kasetsart U.
"""

import sys


class AutomataWithOutput:
    def __init__(self, moves, error_moves, start):
        self.moves = moves
        self.error_moves = error_moves
        self.start = start
        self.state = start

    def move(self, inp):
        move = [i for i in self.moves if i[0] == self.state and inp in i[1]]
        if len(move) == 0:
            before_state = self.state
            self.state = "error"
            in_error = [i[1] for i in self.error_moves if i[0] == before_state]
            if len(in_error) > 0:
                return in_error[0]
        else:
            self.state = move[0][2]
            return move[0][3]


class Lexer:
    numerics = list("0123456789")
    characters = list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
    operators = list("+-*/()=;?$")
    dot = ["."]
    whitespaces = [" ", "\n", "\r", "\t"]
    terminator = ["\0"]

    moves = [
        ("start", terminator, "terminated", None),
        ("start", operators, "literals", None),
        ("start", whitespaces, "start", None),
        ("start", characters, "identifiers", None),
        ("start", numerics, "constants", None),
        ("literals", operators, "literals", "lit"),
        ("literals", terminator, "terminated", "lit"),
        ("literals", whitespaces, "start", "lit"),
        ("literals", numerics, "constants", "lit"),
        ("literals", characters, "identifiers", "lit"),
        ("identifiers", characters, "identifiers", None),
        ("identifiers", numerics, "identifiers", None),
        ("identifiers", operators, "literals", "id"),
        ("identifiers", terminator, "terminated", "id"),
        ("identifiers", whitespaces, "start", "id"),
        ("constants", numerics, "constants", None),
        ("constants", whitespaces, "start", "con"),
        ("constants", terminator, "terminated", "con"),
        ("constants", operators, "literals", "con"),
        ("constants", characters, "identifiers", "con"),
        ("constants", dot, "constants-dot", None),
        ("constants-dot", terminator, "terminated", "err"),
        ("constants-dot", numerics, "constant-decimals", None),
        ("constants-dot", characters, "identifiers", "err"),
        ("constants-dot", operators, "literals", "err"),
        ("constant-decimals", numerics, "constant-decimals", None),
        ("constant-decimals", whitespaces, "start", "con"),
        ("constant-decimals", terminator, "terminated", "con"),
        ("constant-decimals", operators, "literals", "con"),
        ("constant-decimals", characters, "identifiers", "con"),
        ("identifiers", dot, "dot-error", "id"),
        ("dot-error", terminator, "terminated", "err"),
        ("dot-error", operators, "literals", "err"),
        ("dot-error", whitespaces, "dot-error", "err"),
        ("dot-error", characters, "identifiers", "err"),
        ("dot-error", numerics, "constants", "err"),
        ("error", terminator, "terminated", "err"),
        ("error", whitespaces, "start", "err"),
        ("error", numerics, "constants", "err"),
        ("error", operators, "literals", "err"),
        ("error", characters, "identifiers", "err"),
    ]

    error_moves = [
        ("start", None),
        ("identifiers", "id"),
        ("literals", "lit"),
        ("constants", "con"),
        ("constants-dot", None),
        ("constant-decimals", "con"),
        ("error", "err"),
    ]

    def __init__(self, debug=False):
        self.fa = AutomataWithOutput(self.moves, self.error_moves, "start")
        self.debug = debug
        self.results = []

    def single_move(self, char):
        return self.fa.move(char)

    def analyse(self, string):
        self.fa.state = "start"
        res = []
        part = ""
        string += "\0"
        for i in string:
            part += i
            output = self.single_move(i)
            if self.debug:
                print("{} {} {}".format(i, self.fa.state, output))
            if output != None:
                res.append((part[:-1].strip(), output))
                part = i.strip()

        return res


class Parser:
    nonterminals = ["S", "E", "Ep", "T", "Tp", "F", "A"]
    terminals = list("+-*/()=;?$")
    rules = {
        "S": {
            "id": ["id", "=", "E", ";", "S"],
            "con": [""],
            "+": [""],
            "-": [""],
            "*": [""],
            "/": [""],
            "(": [""],
            ")": [""],
            ";": [""],
            "=": [""],
            "?": ["?", "S"],
            "$": [""],
        },
        "E": {
            "id": ["T", "Ep"],
            "con": ["T", "Ep"],
            "+": ["T", "Ep"],
            "-": ["T", "Ep"],
            "*": ["T", "Ep"],
            "/": ["T", "Ep"],
            "(": ["T", "Ep"],
            ")": ["T", "Ep"],
            ";": ["T", "Ep"],
            "=": ["T", "Ep"],
            "?": ["T", "Ep"],
            "$": ["T", "Ep"],
        },
        "Ep": {
            "id": [""],
            "con": [""],
            "+": ["+", "T", "Ep"],
            "-": ["-", "T", "Ep"],
            "*": [""],
            "/": [""],
            "(": [""],
            ")": [""],
            ";": [""],
            "=": [""],
            "?": [""],
            "$": [""],
        },
        "T": {
            "id": ["F", "Tp"],
            "con": ["F", "Tp"],
            "+": ["F", "Tp"],
            "-": ["F", "Tp"],
            "*": ["F", "Tp"],
            "/": ["F", "Tp"],
            "(": ["F", "Tp"],
            ")": ["F", "Tp"],
            ";": ["F", "Tp"],
            "=": ["F", "Tp"],
            "?": ["F", "Tp"],
            "$": ["F", "Tp"],
        },
        "Tp": {
            "id": [""],
            "con": [""],
            "+": [""],
            "-": [""],
            "*": ["*", "F", "Tp"],
            "/": ["/", "F", "Tp"],
            "(": [""],
            ")": [""],
            ";": [""],
            "=": [""],
            "?": [""],
            "$": [""],
        },
        "F": {
            "id": ["id", "A"],
            "con": ["con"],
            "+": False,
            "-": False,
            "*": False,
            "/": False,
            "(": ["(", "E", ")"],
            ")": False,
            ";": False,
            "=": False,
            "?": False,
            "$": False,
        },
        "A": {
            "id": [""],
            "con": [""],
            "+": [""],
            "-": [""],
            "*": [""],
            "/": [""],
            "(": ["(", "E", ")"],
            ")": [""],
            ";": [""],
            "=": [""],
            "?": [""],
            "$": [""],
        },
    }

    def __init__(self, debug=False):
        self.debug = debug
        self.last_output = ""

    def parse(self, inp):
        self.inp = inp
        l = Lexer()
        tokens = l.analyse(inp)
        tokens.append(("$", "lit"))
        stack = ["S"]
        pos = 0
        while len(tokens) > 0:
            if self.debug:
                print(stack)
                print(tokens)
                print("{}".format(pos))
            output = "L=> " + " ".join([i for i in stack if i != ""]).strip()
            if output != self.last_output:
                print(output)
                self.last_output = output
            if pos >= len(stack) and len(tokens) > 0:
                print("parse error")
                break
            else:
                if stack[pos] in Parser.nonterminals:
                    if tokens[0][1] == "lit":
                        lookahead = self.rules[stack[pos]][tokens[0][0]]
                    else:
                        lookahead = self.rules[stack[pos]][tokens[0][1]]
                    if lookahead != False:
                        stack[pos : pos + 1] = lookahead
                    else:
                        print("parse error")
                        break
                else:
                    if stack[pos] == "":
                        if tokens[0][0] == "$" and pos == len(stack) - 1:
                            del tokens[0]
                        del stack[pos]
                    elif stack[pos] in Parser.terminals:
                        if tokens[0][1] == "lit":
                            if stack[pos] != tokens[0][0]:
                                print("parse error")
                                break
                        elif tokens[0][1] == "con":
                            print("parse error")
                            break
                        del tokens[0]
                        pos += 1
                    elif stack[pos] == tokens[0][1]:
                        del tokens[0]
                        pos += 1
                    else:
                        print("parse error")
                        break
            if self.debug:
                print("----------")


if __name__ == "__main__":
    p = Parser(debug=False)
    inp = "".join(sys.stdin.readlines())
    p.parse(inp)
