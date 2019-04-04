# (c) 2019 Alexander Korzun
# This file is licensed under the MIT license. See LICENSE file


from . import posinfo

import re


class LexerError(Exception):
    """
    A generic error occuring in the lexer
    """
    pass


class NoMatchingTokenError(LexerError):
    """
    An error when no matching token was found during the process of tokenization

    See also:
        Lexer.tokenize
    """
    def __init__(self, data, offset):
        """
        Constructor

        Arguments:
            data and offset indicate position in the source file where the error occured
        """
        self.data   = data
        self.offset = offset


class AmbiguousTokenError(LexerError):
    """
    An error when multiple longest matching tokens were found during the process of tokenization

    See also:
        Lexer.tokenize
    """
    def __init__(self, data, offset):
        """
        Constructor

        Arguments:
            data and offset indicate position in the source file where the error occured
        """
        self.data   = data
        self.offset = offset


class Rule(object):
    """
    A class representing a token matching rule
    """
    
    def match(self, data, offset):
        """
        Find the longest match in the specified string

        Warning: this method should not be overridden

        Arguments:
            data   - string input
            offset - offset in `data`

        Returns:
            tuple: (
                length of the match,
                matching Token object  OR  None (if token does not match)
            )

        Raises:
            None, but this method in derived classes can raise arbitrary exception
        """
        length = self.get_length(data, offset)
        if length <= 0:
            return length, None
        token_obj = self.make_token(data, offset, length)
        return length, token_obj

    def get_length(self, data, offset):
        """
        Return the length of the longest match

        Override this method to add matching logic

        Arguments:
            data   - string input
            offset - offset in `data`

        Returns:
            the required length. Zero or negative value means no match

        Raises:
            None, but this method in derived classes can raise arbitrary exception
        """
        return 0

    def make_token(self, data, offset, length):
        """
        Return the matching Token object

        Override this method to add more complex matching logic

        Default version constructs an object of type self.get_token_type() from the matching string (see the code)

        Arguments:
            data   - string input
            offset - offset in `data`
            length - value returned from self.get_length(), guaranted to be positive

        Returns:
            the matching Token object. This method in derived classes should not return None
            because it indicates an error in the program logic (self.get_length() returned positive length).
            However, this value will be accepted as absence of match. Future versions of the library may
            issue a warning in such case

        Raises:
            The same as self.TokenType.__init__ raises, but this method in derived classes can raise
            other exceptions
        """
        return self.get_token_type()(data[offset : offset+length], pi=posinfo.from_data(data, offset))

    def get_token_type(self):
        """
        Return the token class for the default version of the self.make_token() method

        Override this method to specify another token class. Overriding is typically achieved by
        usage of lexer_rules.Attach class

        Arguments:
            None

        Returns:
            the required class

        Raises:
            None, and this method in the derived classes should not raise any exceptions
        """
        return SimpleToken


class Token(object):
    """
    A class representing an abstract token
    """
    def __init__(self, pi):
        """
        Constructor

        Arguments:
            pi - posinfo.Posinfo object describing the position of this token in the source file

        Raises:
            None
        """
        self._posinfo = pi
    
    def __repr__(self):
        """
        String representation for debug purposes
        """
        return '{}({}) [at {}]'.format(self.__class__.__name__, str(self), str(self._posinfo))

    def __str__(self):
        """
        String representation of the value of the token (if applicable)
        """
        return ''

    def __eq__(self, other):
        """
        Test two tokens for equality
        """
        return type(self) is type(other) and self._posinfo == other._posinfo

    def __ne__(self, other):
        """
        Test two tokens for inequality
        """
        return not (self == other)


class SimpleToken(Token):
    """
    Simple token holding only the string passed as an argument to __init__ method

    Should however be OK in most of cases. For debug purposes, you may find no-op inheritance useful, for example:
        
        class MyToken(SimpleToken):
            pass

    Arguments:
        (see Token.__init__)
        content - a string forming the token
    """
    def __init__(self, content, pi):
        """
        Constructor

        Arguments:
            content - string to hold
            pi      - posinfo.Posinfo object representing the position of this token in the source file

        Raises:
            None
        """
        super().__init__(pi)
        self.content = str(content)
        
    def __str__(self):
        return self.content

    def __eq__(self, other):
        return super().__eq__(other) and self.content == other.content


class Lexer(object):
    """
    A class for converting string input into a sequnce of tokens
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.token_specs = []

    def add(self, rule, ignore=False):
        """
        Add a token specification

        Arguments:
            rule   - rule for reading the token (Rule object)
            ignore - if true, the token will be ignored

        Returns:
            None

        Raises:
            None
        """
        self.token_specs.append({'rule': rule, 'ignore': ignore})

    def tokenize(self, data):
        """
        Convert string input into a sequnce of tokens

        Arguments:
            data - string input

        Yields:
            Current token, if not ignored

        Raises:
            NoMatchingTokenError if no matching token was found
            AmbiguousTokenError  if multiple tokens with same length match
        """
        offset = 0
        while offset < len(data):
            # While not EOF
            length, token = self._next_token(data, offset)
            if not token['spec']['ignore']:
                yield token['token']
            offset += length
    
    def _next_token(self, data, offset):
        """
        Get the next token

        Internal method

        Arguments:
            data   - string input
            offset - current offset

        Returns:
            tuple: (
                length of the token,
                dict: {
                    'spec':  specification of the matching token,
                    'token': the matching Token object
                }
            )

        Raises:
            NoMatchingTokenError if no matching token was found
            AmbiguousTokenError  if multiple tokens with same length match
        """
        
        matches = []

        for spec in self.token_specs:
            rule = spec['rule']
            length, token_obj = rule.match(data, offset)
            if length <= 0 or token_obj is None:
                continue
            matches.append((length, token_obj, spec))

        # If nothing was found, raise NoMatchingTokenError
        if len(matches) == 0:
            raise NoMatchingTokenError(data=data, offset=offset)

        # If only one matching token was found, return it
        if len(matches) == 1:
            length, token_obj, spec = matches[0]
            return length, {'spec': spec, 'token': token_obj}

        # If multiple matching tokens were found, choose the longest matching
        # Firstly, we sort the resulting list. It is needed to find two longest tokens (see below).
        # It could have been done more efficiently (a) manually, iterating through the list and maintaining
        # two maximal values or (b) using heapq module. However, first method isn't pythonic (and I believe
        # the code I write for this lib has to be pythonic and simple) and the second method doesn't let
        # me specify a custom key function, which is needed to sort only by length.
        matches.sort(key = lambda match: match[0])  # Sort by length

        # Extract two longest matches
        first_longest  = matches[-1] 
        second_longest = matches[-2]

        # If they have the same length, the matching is ambiguous
        if first_longest[0] == second_longest[0]:
            raise AmbiguousTokenError(data=data, offset=offset)

        # Otherwise, return the longest one
        length, token_obj, spec = first_longest
        return length, {'spec': spec, 'token': token_obj}
