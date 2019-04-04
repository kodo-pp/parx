from parx.posinfo import Posinfo
from parx.lexer import *
from parx.lexer_rules import *

import pytest


class LToken(SimpleToken):
    pass


class MToken(SimpleToken):
    pass


class RToken(SimpleToken):
    pass



lexer = Lexer()

l_rule = Attach(LToken, Regex(r'[qwert]+'))
m_rule = Attach(MToken, Regex(r'[rtyu]+'))
r_rule = Attach(RToken, Regex(r'[yuiop]+'))
ws     = String('\n')

lexer.add(l_rule)
lexer.add(m_rule, priority=1)
lexer.add(r_rule, priority=1)
lexer.add(ws, ignore=True)

P = Posinfo


def test1():
    input1 = 'rtrtrt'
    output1 = list(lexer.tokenize(input1))
    assert output1 == [
        MToken ('rtrtrt', P(1, 1)),
    ]


def test2():
    input2 = 'rtrtrte'
    output2 = list(lexer.tokenize(input2))
    assert output2 == [
        LToken ('rtrtrte', P(1, 1)),
    ]


def test3():
    input3 = 'yuyuyu'
    with pytest.raises(AmbiguousTokenError):
        output3 = list(lexer.tokenize(input3))


def test4():
    input4 = 'qwert\nyui\nopoi\nuytrewq'
    output4 = list(lexer.tokenize(input4)) 
    assert output4 == [
        LToken ('qwert', P(1, 1)),
        RToken ('yui',   P(2, 1)),
        RToken ('opoi',  P(3, 1)),
        MToken ('uytr',  P(4, 1)),
        LToken ('ewq',   P(4, 5)),
    ]
