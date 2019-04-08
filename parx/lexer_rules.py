# (c) 2019 Alexander Korzun
# This file is licensed under MIT license. See LICENSE file


from . import lexer

import re


class String(lexer.Rule):
    """
    Lexer rule to match an exact string
    """
    def __init__(self, string):
        """
        Constructor

        Arguments:
            string - string to match

        Raises:
            None
        """
        super().__init__()
        self.string = string

    def get_length(self, data, offset):
        """
        See lexer.Rule.get_length
        """
        length = len(self.string)
        if data[offset : offset + length] == self.string:
            return length
        else:
            return 0


class Regex(lexer.Rule):
    """
    Lexer rule to match a Python regular expression
    """
    def __init__(self, regex):
        """
        Constructor

        Arguments:
            regex - regular expression to match

        Raises:
            None
        """
        super().__init__()
        self.regex = re.compile(regex)

    def get_length(self, data, offset):
        """
        See lexer.Rule.get_length
        """
        match = self.regex.match(data, pos=offset)
        if match is None:
            return 0
        else:
            return match.end() - match.start()


class Attach(lexer.Rule):
    """
    Lexer rule to specify which token class to instantiate while matching

    Modifies already existing rule. Cannot be used when the rule object has custom
    make_token method
    """
    def __init__(self, token_class, rule):
        """
        Constructor

        Arguments:
            token_class - token class to use
            rule        - existing tule to alter

        Raises:
            None if `rule` is a valid Rule object (which it should be).
            Otherwise, AttributeError (and maybe other exceptions) may be raised
        """
        super().__init__()
        self.token_class = token_class
        self.rule = rule

    def get_length(self, *args):
        return self.rule.get_length(*args)

    def get_token_type(self):
        """
        See lexer.Rule.get_token_type
        """
        return self.token_class


class IgnoreValue(lexer.Token):
    """
    Token wrapper used to ignore the value of token when doing comparisons
    """
    def __init__(self, token):
        super().__init__(pi=token._posinfo)
        self.token = token

    def is_identical(self, other):
        return type(self.token) is type(other)
