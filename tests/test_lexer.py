import unittest
from dessa.token import (
    Token, LET, IDENT, ASSIGN, INT, SEMICOLON, EOF,
    PLUS, MINUS, ASTERISK, SLASH, BANG, LT, GT, EQ, NOT_EQ,
    LPAREN, RPAREN, LBRACE, RBRACE, COMMA, ILLEGAL
)
from dessa.lexer import Lexer

class LexerTest(unittest.TestCase):
    def test_let_statement(self):
        input_code = "let x = 5;"
        expected_tokens = [
            Token(LET, "let"),
            Token(IDENT, "x"),
            Token(ASSIGN, "="),
            Token(INT, "5"),
            Token(SEMICOLON, ";"),
            Token(EOF, ""),
        ]

        lexer = Lexer(input_code)

        for expected_token in expected_tokens:
            token = lexer.next_token()
            self.assertEqual(token.type, expected_token.type)
            self.assertEqual(token.literal, expected_token.literal)

    def test_operators_and_delimiters(self):
        input_code = "=+(){},;"
        expected_tokens = [
            Token(ASSIGN, "="),
            Token(PLUS, "+"),
            Token(LPAREN, "("),
            Token(RPAREN, ")"),
            Token(LBRACE, "{"),
            Token(RBRACE, "}"),
            Token(COMMA, ","),
            Token(SEMICOLON, ";"),
            Token(EOF, ""),
        ]

        lexer = Lexer(input_code)

        for expected_token in expected_tokens:
            token = lexer.next_token()
            self.assertEqual(token.type, expected_token.type)
            self.assertEqual(token.literal, expected_token.literal)

    def test_all_operators(self):
        input_code = "-/* !<>==!="
        expected_tokens = [
            Token(MINUS, "-"),
            Token(SLASH, "/"),
            Token(ASTERISK, "*"),
            Token(BANG, "!"),
            Token(LT, "<"),
            Token(GT, ">"),
            Token(EQ, "=="),
            Token(NOT_EQ, "!="),
            Token(EOF, ""),
        ]

        lexer = Lexer(input_code)

        for expected_token in expected_tokens:
            token = lexer.next_token()
            self.assertEqual(token.type, expected_token.type)
            self.assertEqual(token.literal, expected_token.literal)

    def test_illegal_token(self):
        input_code = "@"
        expected_tokens = [
            Token(ILLEGAL, "@"),
            Token(EOF, ""),
        ]

        lexer = Lexer(input_code)

        for expected_token in expected_tokens:
            token = lexer.next_token()
            self.assertEqual(token.type, expected_token.type)
            self.assertEqual(token.literal, expected_token.literal)

if __name__ == '__main__':
    unittest.main()
