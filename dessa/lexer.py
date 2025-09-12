from dessa.token import Token, lookup_ident, ILLEGAL, ASSIGN, SEMICOLON, EOF, INT

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.position = 0
        self.read_position = 0
        self.char = ''
        self._read_char()

    def _read_char(self):
        if self.read_position >= len(self.source_code):
            self.char = ''  # End of input
        else:
            self.char = self.source_code[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def _skip_whitespace(self):
        while self.char.isspace():
            self._read_char()

    def next_token(self) -> Token:
        self._skip_whitespace()

        token = Token(ILLEGAL, self.char)

        if self.char == '=':
            token = Token(ASSIGN, self.char)
        elif self.char == ';':
            token = Token(SEMICOLON, self.char)
        elif self.char == '\0' or self.char == '' :
            token = Token(EOF, "")
        else:
            if self.char.isalpha() or self.char == '_':
                literal = self._read_identifier()
                token_type = lookup_ident(literal)
                return Token(token_type, literal)
            elif self.char.isdigit():
                literal = self._read_number()
                return Token(INT, literal)

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
