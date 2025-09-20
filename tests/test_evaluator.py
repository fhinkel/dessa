import unittest
from dessa.lexer import Lexer
from dessa.parser import Parser
from dessa.evaluator import eval
from dessa.object import Integer, Boolean, NULL, ReturnValue, Error, Function
from dessa.environment import Environment


class EvaluatorTest(unittest.TestCase):
    def test_eval_integer_expression(self):
        input_code = "5"
        evaluated = self._test_eval(input_code)
        self.assertIsInstance(evaluated, Integer)
        self.assertEqual(evaluated.value, 5)

    def test_eval_boolean_expression(self):
        tests = [("true", True), ("false", False)]

        for input_code, expected in tests:
            with self.subTest(input_code=input_code):
                evaluated = self._test_eval(input_code)
                self.assertIsInstance(evaluated, Boolean)
                self.assertEqual(evaluated.value, expected)

    def test_bang_operator(self):
        tests = [
            ("!true", False),
            ("!false", True),
            ("!5", False),
            ("!!true", True),
            ("!!false", False),
            ("!!5", True),
        ]

        for input_code, expected in tests:
            with self.subTest(input_code=input_code):
                evaluated = self._test_eval(input_code)
                self.assertIsInstance(evaluated, Boolean)
                self.assertEqual(evaluated.value, expected)

    def test_minus_prefix_operator(self):
        tests = [
            ("5", 5),
            ("10", 10),
            ("-5", -5),
            ("-10", -10),
        ]

        for input_code, expected in tests:
            with self.subTest(input_code=input_code):
                evaluated = self._test_eval(input_code)
                self.assertIsInstance(evaluated, Integer)
                self.assertEqual(evaluated.value, expected)

    def test_eval_integer_infix_expression(self):
        tests = [
            ("5 + 5 + 5 + 5 - 10", 10),
            ("2 * 2 * 2 * 2 * 2", 32),
            ("-50 + 100 + -50", 0),
            ("5 * 2 + 10", 20),
            ("5 + 2 * 10", 25),
            ("20 + 2 * -10", 0),
            ("50 / 2 * 2 + 10", 60),
            ("2 * (5 + 10)", 30),
            ("3 * 3 * 3 + 10", 37),
            ("3 * (3 * 3) + 10", 37),
            ("(5 + 10 * 2 + 15 / 3) * 2 + -10", 50),
        ]

        for input_code, expected in tests:
            with self.subTest(input_code=input_code):
                evaluated = self._test_eval(input_code)
                self.assertIsInstance(evaluated, Integer)
                self.assertEqual(evaluated.value, expected)

    def test_eval_boolean_infix_expression(self):
        tests = [
            ("1 < 2", True),
            ("1 > 2", False),
            ("1 < 1", False),
            ("1 > 1", False),
            ("1 == 1", True),
            ("1 != 1", False),
            ("1 == 2", False),
            ("1 != 2", True),
            ("true == true", True),
            ("false == false", True),
            ("true == false", False),
            ("true != false", True),
            ("false != true", True),
            ("(1 < 2) == true", True),
            ("(1 < 2) == false", False),
            ("(1 > 2) == true", False),
            ("(1 > 2) == false", True),
        ]

        for input_code, expected in tests:
            with self.subTest(input_code=input_code):
                evaluated = self._test_eval(input_code)
                self.assertIsInstance(evaluated, Boolean)
                self.assertEqual(evaluated.value, expected)

    def test_if_else_expression(self):
        tests = [
            ("if (true) { 10 }", 10),
            ("if (false) { 10 }", None),
            ("if (1) { 10 }", 10),
            ("if (1 < 2) { 10 }", 10),
            ("if (1 > 2) { 10 }", None),
            ("if (1 > 2) { 10 } else { 20 }", 20),
            ("if (1 < 2) { 10 } else { 20 }", 10),
        ]

        for input_code, expected in tests:
            with self.subTest(input_code=input_code):
                evaluated = self._test_eval(input_code)
                if isinstance(expected, int):
                    self.assertIsInstance(evaluated, Integer)
                    self.assertEqual(evaluated.value, expected)
                else:
                    self.assertIs(evaluated, NULL)

    def test_return_statements(self):
        tests = [
            ("return 10;", 10),
            ("return 10; 9;", 10),
            ("return 2 * 5; 9;", 10),
            ("9; return 2 * 5; 9;", 10),
            (
                """
                if (10 > 1) {
                  if (10 > 1) {
                    return 10;
                  }
                  return 1;
                }
                """,
                10,
            ),
        ]

        for input_code, expected in tests:
            with self.subTest(input_code=input_code):
                evaluated = self._test_eval(input_code)
                self.assertIsInstance(evaluated, Integer)
                self.assertEqual(evaluated.value, expected)

    def test_error_handling(self):
        tests = [
            ("5 + true;", "type mismatch: INTEGER + BOOLEAN"),
            ("5 + true; 5;", "type mismatch: INTEGER + BOOLEAN"),
            ("-true", "unknown operator: -BOOLEAN"),
            ("true + false;", "unknown operator: BOOLEAN + BOOLEAN"),
            ("5; true + false; 5", "unknown operator: BOOLEAN + BOOLEAN"),
            ("if (10 > 1) { true + false; }", "unknown operator: BOOLEAN + BOOLEAN"),
            (
                """
                if (10 > 1) {
                  if (10 > 1) {
                    return true + false;
                  }
                  return 1;
                }
                """,
                "unknown operator: BOOLEAN + BOOLEAN",
            ),
            ("foobar", "identifier not found: foobar"),
        ]

        for input_code, expected_message in tests:
            with self.subTest(input_code=input_code):
                evaluated = self._test_eval(input_code)
                self.assertIsInstance(evaluated, Error)
                self.assertEqual(evaluated.message, expected_message)

    def test_let_statements(self):
        tests = [
            ("let a = 5; a;", 5),
            ("let a = 5 * 5; a;", 25),
            ("let a = 5; let b = a; b;", 5),
            ("let a = 5; let b = a; let c = a + b + 5; c;", 15),
        ]

        for input_code, expected in tests:
            with self.subTest(input_code=input_code):
                evaluated = self._test_eval(input_code)
                self.assertIsInstance(evaluated, Integer)
                self.assertEqual(evaluated.value, expected)

    def test_function_object(self):
        input_code = "fn(x) { x + 2; };"
        evaluated = self._test_eval(input_code)
        self.assertIsInstance(evaluated, Function)
        self.assertEqual(len(evaluated.parameters), 1)
        self.assertEqual(str(evaluated.parameters[0]), "x")
        self.assertEqual(str(evaluated.body), "(x + 2)")

    def test_function_application(self):
        tests = [
            ("let identity = fn(x) { x; }; identity(5);", 5),
            ("let identity = fn(x) { return x; }; identity(5);", 5),
            ("let double = fn(x) { x * 2; }; double(5);", 10),
            ("let add = fn(x, y) { x + y; }; add(5, 5);", 10),
            ("let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", 20),
            ("fn(x) { x; }(5)", 5),
        ]

        for input_code, expected in tests:
            with self.subTest(input_code=input_code):
                evaluated = self._test_eval(input_code)
                self.assertIsInstance(evaluated, Integer)
                self.assertEqual(evaluated.value, expected)

    def test_closures(self):
        input_code = """
        let newAdder = fn(x) {
          fn(y) { x + y };
        };
        let addTwo = newAdder(2);
        addTwo(2);
        """
        evaluated = self._test_eval(input_code)
        self.assertIsInstance(evaluated, Integer)
        self.assertEqual(evaluated.value, 4)


    def _test_eval(self, input_code: str):
        lexer = Lexer(input_code)
        parser = Parser(lexer)
        program = parser.parse_program()
        env = Environment()
        evaluated = eval(program, env)
        if isinstance(evaluated, ReturnValue):
            return evaluated.value
        return evaluated



if __name__ == '__main__':
    unittest.main()
