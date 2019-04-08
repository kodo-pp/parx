# (c) 2019 Alexander Korzun
# This file is licensed under the MIT license. See LICENSE file


from . import posinfo
from . import parser


class TokenSequence(parser.Rule):
    """
    A parser rule matching the specified token sequence (ignoring posinfo)
    """
    def __init__(self, sequence):
        """
        Constructor

        Arguments:
            sequence - the token sequence described above

        Raises:
            None
        """
        self.sequence = sequence

    def match(self, tokens, offset):
        """
        see parser.Rule.match
        """
        n = len(self.sequence)
        if offset + n >= len(tokens):
            return 0, None
        if all([a == b for a, b in zip(tokens[offset], self.sequence)):
            
