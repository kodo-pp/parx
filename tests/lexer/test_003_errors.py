from parx.posinfo import Posinfo
from parx.lexer import *
from parx.lexer_rules import *

import pytest


class LessToken(SimpleToken):
    pass


class EvenToken(SimpleToken):
    pass


lexer = Lexer()

less = Attach(LessToken, Regex(r'[0-4]+'))
even = Attach(EvenToken, Regex(r'[02468]+'))

lexer.add(less)
lexer.add(even)

P = Posinfo


def test1():
    input1 = '1386'
    output1 = list(lexer.tokenize(input1))
    assert output1 == [
        LessToken ('13', P(1, 1)),
        EvenToken ('86', P(1, 3)),
    ]


def test2():
    input2 = '13486'
    output2 = list(lexer.tokenize(input2))
    assert output2 == [
        LessToken ('134', P(1, 1)),
        EvenToken ('86',  P(1, 4)),
    ]


def test3():
    input3 = '806346382'
    output3 = list(lexer.tokenize(input3))
    assert output3 == [
        EvenToken ('806', P(1, 1)),
        LessToken ('34',  P(1, 4)),
        EvenToken ('6',   P(1, 6)),
        LessToken ('3',   P(1, 7)),
        EvenToken ('82',  P(1, 8)),
    ]


def test4():
    input4 = '024'
    with pytest.raises(AmbiguousTokenError):
        output4 = list(lexer.tokenize(input4))


def test5():
    input5 = '0246'
    output5 = list(lexer.tokenize(input5))
    assert output5 == [
        EvenToken ('0246', P(1, 1)),
    ]


def test6():
    input6 = '78'
    with pytest.raises(NoMatchingTokenError):
        output6 = list(lexer.tokenize(input6))
