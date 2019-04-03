# (c) 2019 Alexander Korzun
# This file is licensed under MIT license. See LICENSE file


from . import lexer


class String(lexer.Rule):
    def __init__(self, string):
        super().__init__()
        self.string = string

    def get_length(self, data, offset):
        length = len(self.string)
        if data[offset : offset + length] == self.string:
            return length
        else:
            return 0


class Regex(lexer.Rule):
    def __init__(self, regex):
        super().__init__()
        self.regex = regex

    def get_length(self, data, offset):
        match = re.match(regex, data, pos=offset)
        if match is None:
            return 0
        else:
            return match.end - match.start
