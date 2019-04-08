# (c) 2019 Alexander Korzun
# This file is licensed under the MIT license. See LICENSE file


from . import posinfo


class ParserError(Exception):
    """
    A generic error occuring in the parser
    """
    pass


class IncompleteError(ParserError):
    """
    An error when a parser finishes parsing the input but an end of the input was not reached
    """
    def __init__(self, token):
        """
        Constructor

        Arguments:
            token - the first token not covered by the parser rules

        Raises:
            None
        """
        self.token = token

    def __str__(self):
        return str(token)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self.token))


class PostponeMatching(Exception):
    """
    Exception indicating that left recursion was detected and asking to postpone matching of the current
    rule until this situation is resolved
    """
    pass


class SkipRule(Exception):
    """
    Exception indicating that the current rule should be skipped
    """
    pass


class Rule(object):
    """
    Parsing rule

    This base class matches an empty sequence of tokens
    """
    def match(self, tokens, offset):
        """
        Perform matching

        Arguments:
            tokens - token sequence
            offset - offset in that sequence

        Returns:
            (lenght, node) tuple. Length is the number of consumed tokens, node is the AST node

        Raises:
            None
        """
        return 0, None


class Node(object):
    """
    AST node
    """
    def __init__(self, value=None, pi=None):
        self.value = value
        self._posinfo = pi

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '{}({}) [at {}]'.format(self.__class__.__name__, repr(self.value), str(self._posinfo))

    def __eq__(self, other):
        return type(self) is type(other) and self.value == other.value and self._posinfo == other._posinfo

    def __ne__(self, other):
        return not (self == other)

    def is_identical(self, other):
        return type(self) is type(other) and self.value == other.value


class Parser(object):
    """
    A class for creating ASTs (Abstract Syntax Trees) from the sequence of tokens
    """
    def __init__(self):
        super().__init__()
        # TODO: insert initialization code if needed
        pass

    def set_root_rule(self, rule):
        """
        Set the rule used to produce the root AST token

        Replaces the current rule, if any

        Arguments:
            rule - parsing rule (an instance of Rule)

        Returns:
            None

        Raises:
            None
        """
        self.root_rule = rule

    def parse(self, tokens):
        """
        Create AST from the sequence of tokens

        Arguments:
            tokens - sequence of tokens (list or an iterator)

        Returns:
            the root node of the resulting AST tree (an instance of Node class)

        Raises:
            UnexpectedTokenError if an unexpected token was encountered
            IncompleteError      if the parsing has finished but the end of the token sequence wasn't reached
        """
        
        # TODO: figure out the syntax error place better
        if type(tokens) is not list:
            tokens = list(tokens)

        #import pudb; pudb.set_trace()
        length, node = self.root_rule.match(tokens, offset=0)
        if length < len(tokens):
            raise IncompleteError(tokens[length])

        return node
