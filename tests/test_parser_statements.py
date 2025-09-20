import unittest
from dessa.ast import ReturnStatement, LetStatement
from dessa.lexer import Lexer
from dessa.parser import Parser


class ParserStatementsTest(unittest.TestCase):
    def test_parse_return_statement(self):
        input_code = "return 5;"
        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ReturnStatement)
        self.assertEqual(stmt.token_literal(), "return")


    def test_parse_let_statement_with_expression(self):
        input_code = "let x = 5 + 5;"
        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, LetStatement)
        self.assertEqual(stmt.token_literal(), "let")
        self.assertEqual(stmt.name.value, "x")
        self.assertIsNotNone(stmt.value)

    def test_parse_return_statement_with_expression(self):
        input_code = "return 5 + 5;"
        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ReturnStatement)
        self.assertEqual(stmt.token_literal(), "return")
        self.assertIsNotNone(stmt.return_value)

if __name__ == '__main__':
    unittest.main()
