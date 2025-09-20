import unittest
from dessa.ast import IntegerLiteral, ExpressionStatement, PrefixExpression, InfixExpression, IfExpression, BlockStatement, FunctionLiteral, CallExpression
from dessa.lexer import Lexer
from dessa.parser import Parser


class ParserExpressionsTest(unittest.TestCase):
    def test_parse_integer_literal_expression(self):
        input_code = "5;"
        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ExpressionStatement)
        expression = stmt.expression
        self.assertIsInstance(expression, IntegerLiteral)
        self.assertEqual(expression.value, 5)
        self.assertEqual(expression.token_literal(), "5")


    def test_parse_prefix_expression(self):
        prefix_tests = [
            ("!5;", "!", 5),
            ("-15;", "-", 15),
        ]

        for input_code, operator, value in prefix_tests:
            with self.subTest(input_code=input_code):
                lexer = Lexer(input_code)
                parser = Parser(lexer)
                program = parser.parse_program()

                self.assertEqual(len(program.statements), 1)
                stmt = program.statements[0]
                self.assertIsInstance(stmt, ExpressionStatement)
                expression = stmt.expression
                self.assertIsInstance(expression, PrefixExpression)
                self.assertEqual(expression.operator, operator)
                self.assertIsInstance(expression.right, IntegerLiteral)
                self.assertEqual(expression.right.value, value)
                self.assertEqual(expression.right.token_literal(), str(value))

    def test_parse_infix_expressions(self):
        infix_tests = [
            ("5 + 5;", 5, "+", 5),
            ("5 - 5;", 5, "-", 5),
            ("5 * 5;", 5, "*", 5),
            ("5 / 5;", 5, "/", 5),
            ("5 > 5;", 5, ">", 5),
            ("5 < 5;", 5, "<", 5),
            ("5 == 5;", 5, "==", 5),
            ("5 != 5;", 5, "!=", 5),
        ]

        for input_code, left_value, operator, right_value in infix_tests:
            with self.subTest(input_code=input_code):
                lexer = Lexer(input_code)
                parser = Parser(lexer)
                program = parser.parse_program()

                self.assertEqual(len(program.statements), 1)
                stmt = program.statements[0]
                self.assertIsInstance(stmt, ExpressionStatement)
                expression = stmt.expression
                self.assertIsInstance(expression, InfixExpression)
                self.assertIsInstance(expression.left, IntegerLiteral)
                self.assertEqual(expression.left.value, left_value)
                self.assertEqual(expression.operator, operator)
                self.assertIsInstance(expression.right, IntegerLiteral)
                self.assertEqual(expression.right.value, right_value)

    def test_operator_precedence_parsing(self):
        precedence_tests = [
            ("-a * b", "((-a) * b)"),
            ("!-a", "(!(-a))"),
            ("a + b + c", "((a + b) + c)"),
            ("a + b - c", "((a + b) - c)"),
            ("a * b * c", "((a * b) * c)"),
            ("a * b / c", "((a * b) / c)"),
            ("a + b / c", "(a + (b / c))"),
            ("a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)"),
            ("3 + 4; -5 * 5", "(3 + 4)((-5) * 5)"),
            ("5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"),
            ("5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))"),
            ("3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),
            ("true", "true"),
            ("false", "false"),
            ("3 > 5 == false", "((3 > 5) == false)"),
            ("3 < 5 == true", "((3 < 5) == true)"),
            ("1 + (2 + 3) + 4", "((1 + (2 + 3)) + 4)"),
            ("(5 + 5) * 2", "((5 + 5) * 2)"),
            ("2 / (5 + 5)", "(2 / (5 + 5))"),
            ("-(5 + 5)", "(-(5 + 5))"),
            ("!(true == true)", "(!(true == true))"),
        ]

        for input_code, expected_str in precedence_tests:
            with self.subTest(input_code=input_code):
                lexer = Lexer(input_code)
                parser = Parser(lexer)
                program = parser.parse_program()

                self.assertEqual(str(program), expected_str)

    def test_parse_if_expression(self):
        input_code = "if (x < y) { x }"
        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ExpressionStatement)
        expression = stmt.expression
        self.assertIsInstance(expression, IfExpression)
        self.assertIsInstance(expression.condition, InfixExpression)
        self.assertEqual(str(expression.condition), "(x < y)")
        self.assertIsInstance(expression.consequence, BlockStatement)
        self.assertEqual(len(expression.consequence.statements), 1)
        consequence_stmt = expression.consequence.statements[0]
        self.assertIsInstance(consequence_stmt, ExpressionStatement)
        self.assertEqual(str(consequence_stmt), "x")
        self.assertIsNone(expression.alternative)

    def test_parse_if_else_expression(self):
        input_code = "if (x < y) { x } else { y }"
        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ExpressionStatement)
        expression = stmt.expression
        self.assertIsInstance(expression, IfExpression)
        self.assertIsInstance(expression.condition, InfixExpression)
        self.assertEqual(str(expression.condition), "(x < y)")
        self.assertIsInstance(expression.consequence, BlockStatement)
        self.assertEqual(len(expression.consequence.statements), 1)
        consequence_stmt = expression.consequence.statements[0]
        self.assertIsInstance(consequence_stmt, ExpressionStatement)
        self.assertEqual(str(consequence_stmt), "x")
        self.assertIsNotNone(expression.alternative)
        self.assertIsInstance(expression.alternative, BlockStatement)
        self.assertEqual(len(expression.alternative.statements), 1)
        alternative_stmt = expression.alternative.statements[0]
        self.assertIsInstance(alternative_stmt, ExpressionStatement)
        self.assertEqual(str(alternative_stmt), "y")

    def test_parse_function_literal(self):
        input_code = "fn(x, y) { x + y; }"
        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ExpressionStatement)
        expression = stmt.expression
        self.assertIsInstance(expression, FunctionLiteral)
        self.assertEqual(len(expression.parameters), 2)
        self.assertEqual(str(expression.parameters[0]), "x")
        self.assertEqual(str(expression.parameters[1]), "y")
        self.assertEqual(len(expression.body.statements), 1)
        body_stmt = expression.body.statements[0]
        self.assertIsInstance(body_stmt, ExpressionStatement)
        self.assertEqual(str(body_stmt), "(x + y)")

    def test_parse_call_expression(self):
        input_code = "add(1, 2 * 3, 4 + 5);"
        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ExpressionStatement)
        expression = stmt.expression
        self.assertIsInstance(expression, CallExpression)
        self.assertEqual(str(expression.function), "add")
        self.assertEqual(len(expression.arguments), 3)
        self.assertEqual(str(expression.arguments[0]), "1")
        self.assertEqual(str(expression.arguments[1]), "(2 * 3)")
        self.assertEqual(str(expression.arguments[2]), "(4 + 5)")

if __name__ == '__main__':
    unittest.main()
