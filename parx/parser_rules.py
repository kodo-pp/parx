# (c) 2019 Alexander Korzun
# This file is licensed under the MIT license. See LICENSE file


from . import posinfo
from . import parser


class TokenSequence(parser.Rule):
    """
    A parser rule matching the specified token sequence (ignoring posinfo)
    """
    def __init__(self, sequence, NodeType):
        """
        Constructor

        Arguments:
            sequence - the token sequence described above
            NodeType - class of the AST node which will be returned from match()

        Raises:
            ValueError if the sequence is empty
        """
        if len(sequence) == 0:
            raise ValueError('The sequence is empty')
        self.sequence = sequence
        self.NodeType = NodeType

    def match(self, tokens, offset):
        """
        see parser.Rule.match
        """
        n = len(self.sequence)
        if offset + n > len(tokens):
            return 0, None
        if all([a.is_identical(b) for a, b in zip(self.sequence, tokens[offset : offset + n])]):
            return n, self.NodeType(tokens[offset : offset + n], pi=tokens[offset]._posinfo)
        else:
            return 0, None


class AnyOf(parser.Rule):
    """
    A parser rule matching any of the specified sub-rules
    """
    def __init__(self, rules, NodeType=None):
        """
        Constructor

        Arguments:
            rules - sub-rules described above
            NodeType - class of the AST node which will be returned from match(). None means do not alter the
                       node returned from the sub-rule

        Raises:
            None
        """
        self.rules = rules
        self.NodeType = NodeType

    def match(self, tokens, offset):
        """
        see parser.Rule.match
        """
        # Basically, just match the longest rule, watching out for not having two matching rules of the same
        # length
        matches = []
        for rule in self.rules:
            # TODO: handle left recursion gracefully
            length, node = rule.match(tokens, offset)
            matches.append((length, node))

        matches.sort(key = lambda match: match[0])
        if len(matches) == 0:
            # No matches
            return 0, None
        elif len(matches) == 1:
            return matches[0]
        else:
            first, second = matches[-1], matches[-2]
            if first[0] == second[0]:
                # Ambiguous match
                return 0, None
            if self.NodeType is None:
                return first
            else:
                return first[0], self.NodeType(first[1])


class Optional(parser.Rule):
    """
    A parser rule matching the specified sub-rule or skipping it if the matching failed
    """
    def __init__(self, rule, NodeType=None):
        """
        Constructor

        Arguments:
            rule - sub-rule described above
            NodeType - class of the AST node which will be returned from match(). None means do not alter the
                       node returned from the sub-rule

        Raises:
            None
        """
        self.rule = rule
        self.NodeType = NodeType

    def match(self, tokens, offset):
        """
        see parser.Rule.match
        """
        length, node = self.rule.match(tokens, offset)
        if length <= 0 or node is None:
            raise parser.SkipRule()
        else:
            if self.NodeType is None:
                return length, node
            else:
                return length, self.NodeType(node)


class OneOrMore(parser.Rule):
    """
    A parser rule matching the specified sub-rule repeated once or more
    """
    def __init__(self, rule, NodeType):
        """
        Constructor

        Arguments:
            rule - sub-rule described above
            NodeType - class of the AST node which will be returned from match()

        Raises:
            None
        """
        self.rule = rule
        self.NodeType = NodeType

    def match(self, tokens, offset):
        """
        see parser.Rule.match
        """
        matches = []
        while True:
            length, node = self.rule.match(tokens, offset)
            if length <= 0 or node is None:
                break
            matches.append((length, node))
            offset += length
        if len(matches) == 0:
            return 0, None
        total_length = sum([match[0] for match in matches])
        nodes = [match[1] for match in matches]
        if len(nodes) == 0:
            return 0, None
        return total_length, self.NodeType(nodes, pi=nodes[0]._posinfo)
