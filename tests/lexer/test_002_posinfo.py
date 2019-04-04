from parx.posinfo import Posinfo
from parx.lexer import *
from parx.lexer_rules import *

import pytest


lexer = Lexer()

word    = Regex(r'[a-z]+')
newline = String('\n')
other   = Regex(r'[^a-z\n]+')

lexer.add(word)
lexer.add(newline)
lexer.add(other, ignore=True)

P = Posinfo


def test1():
    input1 = 'foo bar\n\n77baz\n\r  ;'
    output1 = list(lexer.tokenize(input1))
    assert output1 == [
        SimpleToken ('foo', P(1, 1)),
        SimpleToken ('bar', P(1, 5)),
        SimpleToken ('\n',  P(1, 8)),
        SimpleToken ('\n',  P(2, 1)),
        SimpleToken ('baz', P(3, 3)),
        SimpleToken ('\n',  P(3, 6)),
    ]


def test2():
    input2 = '\na\r\nb'
    output2 = list(lexer.tokenize(input2))
    assert output2 == [
        SimpleToken ('\n', P(1, 1)),
        SimpleToken ('a',  P(2, 1)),
        SimpleToken ('\n', P(2, 3)),
        SimpleToken ('b',  P(3, 1)),
    ]
