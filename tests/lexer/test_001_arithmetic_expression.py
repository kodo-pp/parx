from parx.posinfo import Posinfo
from parx.lexer import *
from parx.lexer_rules import *

import pytest


class NumberToken(SimpleToken):
    pass


class VariableToken(SimpleToken):
    pass


class OperatorToken(SimpleToken):
    pass


class WhitespaceToken(SimpleToken):
    pass


def test_arithmetic_expression():
    lexer = Lexer()

    whitespace = Attach(WhitespaceToken, Regex(r'[ \t\n\r]+'))
    number     = Attach(NumberToken,     Regex(r'[+-]?[1-9][0-9]*'))
    variable   = Attach(VariableToken,   Regex(r'[a-zA-Z_][a-zA-Z0-9_]*'))
    operator   = Attach(OperatorToken,   Regex(r'[-+*/%]'))

    lexer.add(whitespace, ignore=True)
    lexer.add(number)
    lexer.add(variable)
    lexer.add(operator)

    P = Posinfo
    input1 = '5 + 6-  \t \r49 * m%3\n/ fooo_o2'
    output1 = list(lexer.tokenize(input1))
    assert output1 == [
        NumberToken   ('5',       P(1, 1)),
        OperatorToken ('+',       P(1, 3)),
        NumberToken   ('6',       P(1, 5)),
        OperatorToken ('-',       P(1, 6)),
        NumberToken   ('49',      P(1, 12)),
        OperatorToken ('*',       P(1, 15)),
        VariableToken ('m',       P(1, 17)),
        OperatorToken ('%',       P(1, 18)),
        NumberToken   ('3',       P(1, 19)),
        OperatorToken ('/',       P(2, 1)),
        VariableToken ('fooo_o2', P(2, 3)),
    ]

    input2 = 'f * 2 4094 -- -4 ---5'
    output2 = list(lexer.tokenize(input2))
    assert output2 == [
        VariableToken ('f',    P(1, 1)),
        OperatorToken ('*',    P(1, 3)),
        NumberToken   ('2',    P(1, 5)),
        NumberToken   ('4094', P(1, 7)),
        OperatorToken ('-',    P(1, 12)),
        OperatorToken ('-',    P(1, 13)),
        NumberToken   ('-4',   P(1, 14)),
        OperatorToken ('-',    P(1, 16)),
        OperatorToken ('-',    P(1, 17)),
        NumberToken   ('-5',   P(1, 18)),
    ]

    input3 = '4 @ 8'
    with pytest.raises(NoMatchingTokenError):
        list(lexer.tokenize(input3))

    input4 = ''
    output4 = list(lexer.tokenize(input4))
    assert output4 == []
