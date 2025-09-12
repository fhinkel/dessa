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
            Token(LET, "let"),
            Token(IDENT, "five"),
            Token(ASSIGN, "="),
            Token(INT, "5"),
            Token(SEMICOLON, ";"),
            Token(LET, "let"),
            Token(IDENT, "ten"),
            Token(ASSIGN, "="),
            Token(INT, "10"),
            Token(SEMICOLON, ";"),
            Token(LET, "let"),
            Token(IDENT, "add"),
            Token(ASSIGN, "="),
            Token(FUNCTION, "fn"),
            Token(LPAREN, "("),
            Token(IDENT, "x"),
            Token(COMMA, ","),
            Token(IDENT, "y"),
            Token(RPAREN, ")"),
            Token(LBRACE, "{"),
            Token(IDENT, "x"),
            Token(PLUS, "+"),
            Token(IDENT, "y"),
            Token(SEMICOLON, ";"),
            Token(RBRACE, "}"),
            Token(SEMICOLON, ";"),
            Token(LET, "let"),
            Token(IDENT, "result"),
            Token(ASSIGN, "="),
            Token(IDENT, "add"),
            Token(LPAREN, "("),
            Token(IDENT, "five"),
            Token(COMMA, ","),
            Token(IDENT, "ten"),
            Token(RPAREN, ")"),
            Token(SEMICOLON, ";"),
            Token(BANG, "!"),
            Token(MINUS, "-"),
            Token(SLASH, "/"),
            Token(ASTERISK, "*"),
            Token(INT, "5"),
            Token(SEMICOLON, ";"),
            Token(INT, "5"),
            Token(LT, "<"),
            Token(INT, "10"),
            Token(GT, ">"),
            Token(INT, "5"),
            Token(SEMICOLON, ";"),
            Token(IF, "if"),
            Token(LPAREN, "("),
            Token(INT, "5"),
            Token(LT, "<"),
            Token(INT, "10"),
            Token(RPAREN, ")"),
            Token(LBRACE, "{"),
            Token(RETURN, "return"),
            Token(TRUE, "true"),
            Token(SEMICOLON, ";"),
            Token(RBRACE, "}"),
            Token(ELSE, "else"),
            Token(LBRACE, "{"),
            Token(RETURN, "return"),
            Token(FALSE, "false"),
            Token(SEMICOLON, ";"),
            Token(RBRACE, "}"),
            Token(INT, "10"),
            Token(EQ, "=="),
            Token(INT, "10"),
            Token(SEMICOLON, ";"),
            Token(INT, "10"),
            Token(NOT_EQ, "!="),
            Token(INT, "9"),
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
