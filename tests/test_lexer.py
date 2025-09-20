import unittest
from dessa.token import (
    Token, LET, IDENT, ASSIGN, INT, SEMICOLON, EOF,
    PLUS, MINUS, ASTERISK, SLASH, BANG, LT, GT, EQ, NOT_EQ,
    LPAREN, RPAREN, LBRACE, RBRACE, COMMA, ILLEGAL, FUNCTION,
    TRUE, FALSE, IF, ELSE, RETURN
)
from dessa.lexer import Lexer

class LexerTest(unittest.TestCase):
    def test_let_statement(self):
        input_code = "let x = 5;"
        expected_tokens = [
            Token(LET, "let", 1, 3),
            Token(IDENT, "x", 1, 5),
            Token(ASSIGN, "=", 1, 7),
            Token(INT, "5", 1, 9),
            Token(SEMICOLON, ";", 1, 10),
            Token(EOF, "", 1, 11),
        ]

        lexer = Lexer(input_code)

        for expected_token in expected_tokens:
            token = lexer.next_token()
            self.assertEqual(token.type, expected_token.type)
            self.assertEqual(token.literal, expected_token.literal)
            self.assertEqual(token.line, expected_token.line)
            self.assertEqual(token.column, expected_token.column)

    def test_operators_and_delimiters(self):
        input_code = "=+(){},;"
        expected_tokens = [
            Token(ASSIGN, "=", 1, 1),
            Token(PLUS, "+", 1, 2),
            Token(LPAREN, "(", 1, 3),
            Token(RPAREN, ")", 1, 4),
            Token(LBRACE, "{", 1, 5),
            Token(RBRACE, "}", 1, 6),
            Token(COMMA, ",", 1, 7),
            Token(SEMICOLON, ";", 1, 8),
            Token(EOF, "", 1, 9),
        ]

        lexer = Lexer(input_code)

        for expected_token in expected_tokens:
            token = lexer.next_token()
            self.assertEqual(token.type, expected_token.type)
            self.assertEqual(token.literal, expected_token.literal)
            self.assertEqual(token.line, expected_token.line)
            self.assertEqual(token.column, expected_token.column)

    def test_all_operators(self):
        input_code = "-/* !<>==!="
        expected_tokens = [
            Token(MINUS, "-", 1, 1),
            Token(SLASH, "/", 1, 2),
            Token(ASTERISK, "*", 1, 3),
            Token(BANG, "!", 1, 5),
            Token(LT, "<", 1, 6),
            Token(GT, ">", 1, 7),
            Token(EQ, "==", 1, 8),
            Token(NOT_EQ, "!=", 1, 10),
            Token(EOF, "", 1, 12),
        ]

        lexer = Lexer(input_code)

        for expected_token in expected_tokens:
            token = lexer.next_token()
            self.assertEqual(token.type, expected_token.type)
            self.assertEqual(token.literal, expected_token.literal)
            self.assertEqual(token.line, expected_token.line)
            self.assertEqual(token.column, expected_token.column)

    def test_illegal_token(self):
        input_code = "@"
        expected_tokens = [
            Token(ILLEGAL, "@", 1, 1),
            Token(EOF, "", 1, 2),
        ]

        lexer = Lexer(input_code)

        for expected_token in expected_tokens:
            token = lexer.next_token()
            self.assertEqual(token.type, expected_token.type)
            self.assertEqual(token.literal, expected_token.literal)
            self.assertEqual(token.line, expected_token.line)
            self.assertEqual(token.column, expected_token.column)

    def test_complex_statement(self):
        input_code = '''
        let five = 5;
        let ten = 10;

        let add = fn(x, y) {
          x + y;
        };

        let result = add(five, ten);
        !-/*5;
        5 < 10 > 5;

        if (5 < 10) {
            return true;
        } else {
            return false;
        }

        10 == 10;
        10 != 9;
        '''
        expected_tokens = [
            Token(LET, "let", 2, 9),
            Token(IDENT, "five", 2, 13),
            Token(ASSIGN, "=", 2, 18),
            Token(INT, "5", 2, 20),
            Token(SEMICOLON, ";", 2, 21),
            Token(LET, "let", 3, 9),
            Token(IDENT, "ten", 3, 13),
            Token(ASSIGN, "=", 3, 17),
            Token(INT, "10", 3, 19),
            Token(SEMICOLON, ";", 3, 21),
            Token(LET, "let", 5, 9),
            Token(IDENT, "add", 5, 13),
            Token(ASSIGN, "=", 5, 17),
            Token(FUNCTION, "fn", 5, 19),
            Token(LPAREN, "(", 5, 21),
            Token(IDENT, "x", 5, 22),
            Token(COMMA, ",", 5, 23),
            Token(IDENT, "y", 5, 25),
            Token(RPAREN, ")", 5, 26),
            Token(LBRACE, "{", 5, 28),
            Token(IDENT, "x", 6, 11),
            Token(PLUS, "+", 6, 13),
            Token(IDENT, "y", 6, 15),
            Token(SEMICOLON, ";", 6, 16),
            Token(RBRACE, "}", 7, 9),
            Token(SEMICOLON, ";", 7, 10),
            Token(LET, "let", 9, 9),
            Token(IDENT, "result", 9, 13),
            Token(ASSIGN, "=", 9, 20),
            Token(IDENT, "add", 9, 22),
            Token(LPAREN, "(", 9, 25),
            Token(IDENT, "five", 9, 26),
            Token(COMMA, ",", 9, 30),
            Token(IDENT, "ten", 9, 32),
            Token(RPAREN, ")", 9, 35),
            Token(SEMICOLON, ";", 9, 36),
            Token(BANG, "!", 10, 9),
            Token(MINUS, "-", 10, 10),
            Token(SLASH, "/", 10, 11),
            Token(ASTERISK, "*", 10, 12),
            Token(INT, "5", 10, 13),
            Token(SEMICOLON, ";", 10, 14),
            Token(INT, "5", 11, 9),
            Token(LT, "<", 11, 11),
            Token(INT, "10", 11, 13),
            Token(GT, ">", 11, 16),
            Token(INT, "5", 11, 18),
            Token(SEMICOLON, ";", 11, 19),
            Token(IF, "if", 13, 9),
            Token(LPAREN, "(", 13, 12),
            Token(INT, "5", 13, 13),
            Token(LT, "<", 13, 15),
            Token(INT, "10", 13, 17),
            Token(RPAREN, ")", 13, 19),
            Token(LBRACE, "{", 13, 21),
            Token(RETURN, "return", 14, 13),
            Token(TRUE, "true", 14, 20),
            Token(SEMICOLON, ";", 14, 24),
            Token(RBRACE, "}", 15, 9),
            Token(ELSE, "else", 15, 11),
            Token(LBRACE, "{", 15, 16),
            Token(RETURN, "return", 16, 13),
            Token(FALSE, "false", 16, 20),
            Token(SEMICOLON, ";", 16, 25),
            Token(RBRACE, "}", 17, 9),
            Token(INT, "10", 19, 9),
            Token(EQ, "==", 19, 12),
            Token(INT, "10", 19, 15),
            Token(SEMICOLON, ";", 19, 17),
            Token(INT, "10", 20, 9),
            Token(NOT_EQ, "!=", 20, 12),
            Token(INT, "9", 20, 15),
            Token(SEMICOLON, ";", 20, 16),
            Token(EOF, "", 21, 9),
        ]

        lexer = Lexer(input_code)

        for expected_token in expected_tokens:
            token = lexer.next_token()
            self.assertEqual(token.type, expected_token.type)
            self.assertEqual(token.literal, expected_token.literal)
            self.assertEqual(token.line, expected_token.line)
            self.assertEqual(token.column, expected_token.column)

if __name__ == '__main__':
    unittest.main()
