from parx.posinfo import Posinfo
from parx.lexer import Lexer, SimpleToken
from parx import lexer_rules as lr
from parx.parser import Parser, Node
from parx import parser_rules as pr

import pytest


class WordToken(SimpleToken):
    pass


lexer = Lexer()

whitespace = lr.Regex(r'[ \t\n\r]+')
word       = lr.Attach(WordToken,   lr.Regex(r'[a-zA-Z0-9_-]+'))

lexer.add(whitespace, ignore=True)
lexer.add(word)

P = Posinfo


class HelloNode(Node):
    pass


class GreetingListNode(Node):
    pass


hello = pr.TokenSequence([WordToken('Hello'), lr.IgnoreValue(WordToken())], NodeType=HelloNode)
greeting_list = pr.OneOrMore(hello, NodeType=GreetingListNode)

parser = Parser()
parser.set_root_rule(greeting_list)


def test1():
    string = 'Hello world Hello bar Hello baz'
    tokens = list(lexer.tokenize(string))
    output = parser.parse(tokens)

    assert output == GreetingListNode(
        [
            HelloNode(
                [
                    WordToken('Hello', P(1, 1)),
                    WordToken('world', P(1, 7)),
                ],
                pi=P(1, 1),
            ),
            HelloNode(
                [
                    WordToken('Hello', P(1, 13)),
                    WordToken('bar',   P(1, 19)),
                ],
                pi=P(1, 13),
            ),
            HelloNode(
                [
                    WordToken('Hello', P(1, 23)),
                    WordToken('baz',   P(1, 29)),
                ],
                pi=P(1, 23),
            ),
        ],
        pi=P(1, 1),
    )

    assert output != HelloNode(
        [
            HelloNode(
                [
                    WordToken('Hello', P(1, 1)),
                    WordToken('world', P(1, 7)),
                ],
                pi=P(1, 1),
            ),
            HelloNode(
                [
                    WordToken('Hello', P(1, 13)),
                    WordToken('bar',   P(1, 19)),
                ],
                pi=P(1, 13),
            ),
            HelloNode(
                [
                    WordToken('Hello', P(1, 23)),
                    WordToken('baz',   P(1, 29)),
                ],
                pi=P(1, 23),
            ),
        ],
        pi=P(1, 1),
    )

    assert output != GreetingListNode(
        [
            HelloNode(
                [
                    WordToken('Hello', P(1, 1)),
                    WordToken('world', P(1, 7)),
                ],
                pi=P(1, 1),
            ),
            HelloNode(
                [
                    WordToken('Hello', P(1, 13)),
                    WordToken('bar',   P(1, 19)),
                ],
                pi=P(1, 13),
            ),
            HelloNode(
                [
                    WordToken('Hello', P(1, 23)),
                    WordToken('baz',   P(1, 29)),
                ],
                pi=P(1, 23),
            ),
        ],
        pi=P(1, 2),
    )

    assert output != GreetingListNode(
        [
            HelloNode(
                [
                    WordToken('Hello', P(1, 1)),
                    WordToken('worlz', P(1, 7)),
                ],
                pi=P(1, 1),
            ),
            HelloNode(
                [
                    WordToken('Hello', P(1, 13)),
                    WordToken('bar',   P(1, 19)),
                ],
                pi=P(1, 13),
            ),
            HelloNode(
                [
                    WordToken('Hello', P(1, 23)),
                    WordToken('baz',   P(1, 29)),
                ],
                pi=P(1, 23),
            ),
        ],
        pi=P(1, 1),
    )
    assert output != GreetingListNode(
        [
            HelloNode(
                [
                    WordToken('Hello', P(1, 1)),
                    WordToken('world', P(1, 7)),
                ],
                pi=P(1, 1),
            ),
            HelloNode(
                [
                    WordToken('Hello', P(1, 13)),
                    WordToken('bar',   P(1, 19)),
                ],
                pi=P(1, 13),
            ),
        ],
        pi=P(1, 1),
    )
