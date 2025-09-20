from dessa.token import (
    Token, lookup_ident, ILLEGAL, ASSIGN, SEMICOLON, EOF, INT,
    PLUS, MINUS, ASTERISK, SLASH, BANG, LT, GT, EQ, NOT_EQ,
    LPAREN, RPAREN, LBRACE, RBRACE, COMMA
)

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.position = 0
        self.read_position = 0
        self.char = ''
        self.line = 1
        self.column = 0
        self._read_char()

    def _read_char(self):
        if self.read_position >= len(self.source_code):
            self.char = ''  # End of input
        else:
            self.char = self.source_code[self.read_position]

        if self.char == '\n':
            self.line += 1
            self.column = 0
        else:
            self.column += 1

        self.position = self.read_position
        self.read_position += 1

    def _peek_char(self) -> str:
        if self.read_position >= len(self.source_code):
            return ''
        return self.source_code[self.read_position]

    def _skip_whitespace(self):
        while self.char.isspace():
            self._read_char()

    def next_token(self) -> Token:
        self._skip_whitespace()

        token_line = self.line
        token_column = self.column

        if self.char == '=':
            if self._peek_char() == '=':
                char = self.char
                self._read_char()
                literal = char + self.char
                token = Token(EQ, literal, token_line, token_column)
            else:
                token = Token(ASSIGN, self.char, token_line, token_column)
        elif self.char == ';':
            token = Token(SEMICOLON, self.char, token_line, token_column)
        elif self.char == '+':
            token = Token(PLUS, self.char, token_line, token_column)
        elif self.char == '-':
            token = Token(MINUS, self.char, token_line, token_column)
        elif self.char == '*':
            token = Token(ASTERISK, self.char, token_line, token_column)
        elif self.char == '/':
            token = Token(SLASH, self.char, token_line, token_column)
        elif self.char == '!':
            if self._peek_char() == '=':
                char = self.char
                self._read_char()
                literal = char + self.char
                token = Token(NOT_EQ, literal, token_line, token_column)
            else:
                token = Token(BANG, self.char, token_line, token_column)
        elif self.char == '<':
            token = Token(LT, self.char, token_line, token_column)
        elif self.char == '>':
            token = Token(GT, self.char, token_line, token_column)
        elif self.char == '(':
            token = Token(LPAREN, self.char, token_line, token_column)
        elif self.char == ')':
            token = Token(RPAREN, self.char, token_line, token_column)
        elif self.char == '{':
            token = Token(LBRACE, self.char, token_line, token_column)
        elif self.char == '}':
            token = Token(RBRACE, self.char, token_line, token_column)
        elif self.char == ',':
            token = Token(COMMA, self.char, token_line, token_column)
        elif self.char == '\x00' or self.char == '' :
            token = Token(EOF, "", token_line, token_column)
        else:
            if self.char.isalpha() or self.char == '_':
                literal = self._read_identifier()
                token_type = lookup_ident(literal)
                return Token(token_type, literal, token_line, token_column)
            elif self.char.isdigit():
                literal = self._read_number()
                return Token(INT, literal, token_line, token_column)
            else:
                token = Token(ILLEGAL, self.char, token_line, token_column)

        self._read_char()
        return token

    def _read_identifier(self) -> str:
        start_position = self.position
        while self.char.isalpha() or self.char == '_':
            self._read_char()
        return self.source_code[start_position:self.position]

    def _read_number(self) -> str:
        start_position = self.position
        while self.char.isdigit():
            self._read_char()
        return self.source_code[start_position:self.position]
