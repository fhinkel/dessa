import unittest
from dessa.ast import LetStatement
from dessa.lexer import Lexer
from dessa.parser import Parser


class ParserTest(unittest.TestCase):
    def test_placeholder(self):
        self.assertEqual(1, 1)

    def test_parse_let_statement(self):
        input_code = """
        let x = 5;
        let y = 10;
        let foobar = 838383;
        """
        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertIsNotNone(program)
        self.assertEqual(len(program.statements), 3)

        expected_identifiers = ["x", "y", "foobar"]
        for i, stmt in enumerate(program.statements):
            self.assertIsInstance(stmt, LetStatement)
            self.assertEqual(stmt.token_literal(), "let")
            self.assertEqual(stmt.name.value, expected_identifiers[i])
            self.assertEqual(stmt.name.token_literal(), expected_identifiers[i])


if __name__ == '__main__':
    unittest.main()
