import unittest
from dessa.token import Token, LET, IDENT, ASSIGN, INT, SEMICOLON, EOF
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

if __name__ == '__main__':
    unittest.main()
