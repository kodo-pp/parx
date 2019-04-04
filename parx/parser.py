# (c) 2019 Alexander Korzun
# This file is licensed under the MIT license. See LICENSE file


from . import posinfo


class ParserError(Exception):
    """
    A generic error occuring in the parser
    """
    pass


class UnexpectedTokenError(ParserError):
    """
    An error when a parser encounters a token of a certain type but it doesn't match
    any parsing rule known to the parser
    """
    pass


class IncompleteError(ParserError):
    """
    An error when a parser finishes parsing the input but an end of the input was not reached
    """
    pass


class Rule(object):
    """
    Parsing rule

    This base class matches nothing
    """
    def match(self, tokens, offset):
        


class Parser(object):
    """
    A class for creating ASTs (Abstract Syntax Trees) from the sequence of tokens
    """
    def __init__(self):
        super().__init__()
        # TODO: insert initialization code if needed
        pass

    def add(self, rule):
        """
        Add a parsing rule to the parser

        Arguments:
            rule - parsing rule (an instance of Rule)

        Returns:
            None

        Raises:
            None
        """

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
        if type(tokens) is not list:
            tokens = list(tokens)
        
        # TODO
        raise NotImplementedError()
