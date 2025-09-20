from enum import IntEnum
from dessa.ast import (
    Program,
    LetStatement,
    Identifier,
    Expression,
    ExpressionStatement,
    IntegerLiteral,
    PrefixExpression,
    InfixExpression,
    Boolean,
    ReturnStatement,
    IfExpression,
    BlockStatement,
    FunctionLiteral,
    CallExpression,
)
from dessa.lexer import Lexer
from dessa.token import (
    Token,
    TokenType,
    EOF,
    LET,
    RETURN,
    IDENT,
    ASSIGN,
    SEMICOLON,
    INT,
    BANG,
    MINUS,
    PLUS,
    SLASH,
    ASTERISK,
    EQ,
    NOT_EQ,
    LT,
    GT,
    TRUE,
    FALSE,
    LPAREN,
    RPAREN,
    IF,
    LBRACE,
    RBRACE,
    ELSE,
    FUNCTION,
    COMMA,
)


class Precedence(IntEnum):
    LOWEST = 1
    EQUALS = 2
    LESSGREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    CALL = 7


precedences = {
    EQ: Precedence.EQUALS,
    NOT_EQ: Precedence.EQUALS,
    LT: Precedence.LESSGREATER,
    GT: Precedence.LESSGREATER,
    PLUS: Precedence.SUM,
    MINUS: Precedence.SUM,
    SLASH: Precedence.PRODUCT,
    ASTERISK: Precedence.PRODUCT,
    LPAREN: Precedence.CALL,
}


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._errors: list[str] = []

        self._curr_token: Token | None = None
        self._peek_token: Token | None = None
        self._advance_tokens()
        self._advance_tokens()

        self._prefix_parse_fns = {
            IDENT: self._parse_identifier,
            INT: self._parse_integer_literal,
            BANG: self._parse_prefix_expression,
            MINUS: self._parse_prefix_expression,
            TRUE: self._parse_boolean,
            FALSE: self._parse_boolean,
            LPAREN: self._parse_grouped_expression,
            IF: self._parse_if_expression,
            FUNCTION: self._parse_function_literal,
        }
        self._infix_parse_fns = {
            PLUS: self._parse_infix_expression,
            MINUS: self._parse_infix_expression,
            SLASH: self._parse_infix_expression,
            ASTERISK: self._parse_infix_expression,
            EQ: self._parse_infix_expression,
            NOT_EQ: self._parse_infix_expression,
            LT: self._parse_infix_expression,
            GT: self._parse_infix_expression,
            LPAREN: self._parse_call_expression,
        }

    @property
    def errors(self) -> list[str]:
        return self._errors

    def parse_program(self) -> Program:
        """
        Parses the program and returns the root node of the AST.
        """
        program = Program()

        while self._curr_token and self._curr_token.type != EOF:
            stmt = self._parse_statement()
            if stmt:
                program.statements.append(stmt)
            self._advance_tokens()

        if self.errors:
            raise Exception("\n".join(self.errors))

        return program

    def _advance_tokens(self) -> None:
        """
        Advances the tokens by one.
        """
        self._curr_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    def _parse_statement(self) -> None:
        """
        Parses a statement.
        """
        if self._curr_token:
            if self._curr_token.type == LET:
                return self._parse_let_statement()
            elif self._curr_token.type == RETURN:
                return self._parse_return_statement()
        return self._parse_expression_statement()

    def _parse_let_statement(self) -> LetStatement | None:
        """
        Parses a let statement.
        """
        if not self._curr_token:
            return None

        let_token = self._curr_token

        if not self._expect_peek(IDENT):
            return None

        if not self._curr_token:
            return None

        name = Identifier(token=self._curr_token, value=self._curr_token.literal)

        if not self._expect_peek(ASSIGN):
            return None

        self._advance_tokens()

        value = self._parse_expression(Precedence.LOWEST)

        if self._peek_token and self._peek_token.type == SEMICOLON:
            self._advance_tokens()

        return LetStatement(token=let_token, name=name, value=value)

    def _parse_return_statement(self) -> ReturnStatement | None:
        """
        Parses a return statement.
        """
        if not self._curr_token:
            return None

        stmt = ReturnStatement(token=self._curr_token, return_value=None)

        self._advance_tokens()

        stmt.return_value = self._parse_expression(Precedence.LOWEST)

        if self._peek_token and self._peek_token.type == SEMICOLON:
            self._advance_tokens()

        return stmt

    def _parse_expression_statement(self) -> ExpressionStatement | None:
        """
        Parses an expression statement.
        """
        if not self._curr_token:
            return None

        stmt = ExpressionStatement(token=self._curr_token, expression=self._parse_expression(Precedence.LOWEST))

        if self._peek_token and self._peek_token.type == SEMICOLON:
            self._advance_tokens()

        return stmt

    def _parse_expression(self, precedence: Precedence) -> Expression | None:
        """
        Parses an expression.
        """
        if not self._curr_token:
            return None

        prefix = self._prefix_parse_fns.get(self._curr_token.type)
        if not prefix:
            self._no_prefix_parse_fn_error(self._curr_token.type)
            return None

        left_exp = prefix()

        while self._peek_token and self._peek_token.type != SEMICOLON and precedence < self._peek_precedence():
            infix = self._infix_parse_fns.get(self._peek_token.type)
            if not infix:
                return left_exp

            self._advance_tokens()

            if not left_exp:
                return None

            left_exp = infix(left_exp)

        return left_exp

    def _parse_identifier(self) -> Expression | None:
        """
        Parses an identifier.
        """
        if not self._curr_token:
            return None
        return Identifier(token=self._curr_token, value=self._curr_token.literal)

    def _parse_integer_literal(self) -> Expression | None:
        """
        Parses an integer literal.
        """
        if not self._curr_token:
            return None

        try:
            value = int(self._curr_token.literal)
        except ValueError:
            msg = f"could not parse {self._curr_token.literal} as integer"
            self._errors.append(msg)
            return None

        return IntegerLiteral(token=self._curr_token, value=value)

    def _parse_prefix_expression(self) -> Expression | None:
        """
        Parses a prefix expression.
        """
        if not self._curr_token:
            return None

        expression_token = self._curr_token
        self._advance_tokens()
        right = self._parse_expression(Precedence.PREFIX)

        if not right:
            return None

        return PrefixExpression(token=expression_token, operator=expression_token.literal, right=right)

    def _parse_infix_expression(self, left: Expression) -> Expression | None:
        """
        Parses an infix expression.
        """
        if not self._curr_token:
            return None

        expression_token = self._curr_token
        precedence = self._curr_precedence()
        self._advance_tokens()
        right = self._parse_expression(precedence)

        if not right:
            return None

        return InfixExpression(token=expression_token, left=left, operator=expression_token.literal, right=right)

    def _parse_boolean(self) -> Expression | None:
        """
        Parses a boolean.
        """
        if not self._curr_token:
            return None

        return Boolean(token=self._curr_token, value=self._curr_token.type == TRUE)

    def _parse_grouped_expression(self) -> Expression | None:
        """
        Parses a grouped expression.
        """
        self._advance_tokens()

        exp = self._parse_expression(Precedence.LOWEST)

        if not self._expect_peek(RPAREN):
            return None

        return exp

    def _parse_if_expression(self) -> Expression | None:
        """
        Parses an if expression.
        """
        if not self._curr_token:
            return None

        expression_token = self._curr_token

        if not self._expect_peek(LPAREN):
            return None

        self._advance_tokens()
        condition = self._parse_expression(Precedence.LOWEST)

        if not self._expect_peek(RPAREN):
            return None

        if not self._expect_peek(LBRACE):
            return None

        consequence = self._parse_block_statement()

        alternative = None
        if self._peek_token and self._peek_token.type == ELSE:
            self._advance_tokens()

            if not self._expect_peek(LBRACE):
                return None

            alternative = self._parse_block_statement()

        return IfExpression(token=expression_token, condition=condition, consequence=consequence, alternative=alternative)

    def _parse_block_statement(self) -> BlockStatement | None:
        """
        Parses a block statement.
        """
        if not self._curr_token:
            return None

        block_token = self._curr_token
        statements: list[ExpressionStatement] = []

        self._advance_tokens()

        while self._curr_token and self._curr_token.type != RBRACE and self._curr_token.type != EOF:
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            self._advance_tokens()

        return BlockStatement(token=block_token, statements=statements)

    def _parse_function_literal(self) -> Expression | None:
        """
        Parses a function literal.
        """
        if not self._curr_token:
            return None

        lit_token = self._curr_token

        if not self._expect_peek(LPAREN):
            return None

        parameters = self._parse_function_parameters()

        if not self._expect_peek(LBRACE):
            return None

        body = self._parse_block_statement()

        return FunctionLiteral(token=lit_token, parameters=parameters, body=body)

    def _parse_function_parameters(self) -> list[Identifier]:
        """
        Parses the parameters of a function.
        """
        identifiers: list[Identifier] = []

        if self._peek_token and self._peek_token.type == RPAREN:
            self._advance_tokens()
            return identifiers

        self._advance_tokens()

        if self._curr_token:
            ident = Identifier(token=self._curr_token, value=self._curr_token.literal)
            identifiers.append(ident)

        while self._peek_token and self._peek_token.type == COMMA:
            self._advance_tokens()
            self._advance_tokens()
            if self._curr_token:
                ident = Identifier(token=self._curr_token, value=self._curr_token.literal)
                identifiers.append(ident)

        if not self._expect_peek(RPAREN):
            return []

        return identifiers

    def _parse_call_expression(self, function: Expression) -> Expression | None:
        """
        Parses a call expression.
        """
        if not self._curr_token:
            return None

        exp = CallExpression(token=self._curr_token, function=function, arguments=None)  # type: ignore
        exp.arguments = self._parse_call_arguments()
        return exp

    def _parse_call_arguments(self) -> list[Expression]:
        """
        Parses the arguments of a call expression.
        """
        args: list[Expression] = []

        if self._peek_token and self._peek_token.type == RPAREN:
            self._advance_tokens()
            return args

        self._advance_tokens()

        if self._curr_token:
            arg = self._parse_expression(Precedence.LOWEST)
            if arg:
                args.append(arg)

        while self._peek_token and self._peek_token.type == COMMA:
            self._advance_tokens()
            self._advance_tokens()
            if self._curr_token:
                arg = self._parse_expression(Precedence.LOWEST)
                if arg:
                    args.append(arg)

        if not self._expect_peek(RPAREN):
            return []

        return args

    def _expect_peek(self, token_type: TokenType) -> bool:
        """
        Checks if the peek token is of the expected type.
        """
        if self._peek_token and self._peek_token.type == token_type:
            self._advance_tokens()
            return True
        else:
            self._peek_error(token_type)
            return False

    def _peek_error(self, token_type: TokenType) -> None:
        """
        Adds an error to the parser.
        """
        if self._peek_token:
            msg = f"expected next token to be {token_type}, got {self._peek_token.type} instead"
            self._errors.append(msg)

    def _no_prefix_parse_fn_error(self, token_type: TokenType) -> None:
        """
        Adds an error to the parser.
        """
        msg = f"no prefix parse function for {token_type} found"
        self._errors.append(msg)

    def _peek_precedence(self) -> Precedence:
        """
        Returns the precedence of the peek token.
        """
        if self._peek_token and self._peek_token.type in precedences:
            return precedences[self._peek_token.type]
        return Precedence.LOWEST

    def _curr_precedence(self) -> Precedence:
        """
        Returns the precedence of the current token.
        """
        if self._curr_token and self._curr_token.type in precedences:
            return precedences[self._curr_token.type]
        return Precedence.LOWEST
