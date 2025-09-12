from dataclasses import dataclass

# Supported Token Types
TokenType = str

ILLEGAL = "ILLEGAL"  # A character we don't know about
EOF     = "EOF"      # End of File

# Identifiers + literals
IDENT = "IDENT"  # add, foobar, x, y, ...
INT   = "INT"    # 1343456

# Operators
ASSIGN   = "="
PLUS     = "+"
MINUS    = "-"
BANG     = "!"
ASTERISK = "*"
SLASH    = "/"
LT       = "<"
GT       = ">"
EQ       = "=="
NOT_EQ   = "!="

# Delimiters
COMMA     = ","
SEMICOLON = ";"
LPAREN    = "("
RPAREN    = ")"
LBRACE    = "{"
RBRACE    = "}"

# Keywords
FUNCTION = "FUNCTION"
LET      = "LET"
TRUE     = "TRUE"
FALSE    = "FALSE"
IF       = "IF"
ELSE     = "ELSE"
RETURN   = "RETURN"


@dataclass
class Token:
    type: TokenType
    literal: str
    line: int = 0
    column: int = 0

# A dictionary to look up keywords
keywords: dict[str, TokenType] = {
    "fn": FUNCTION,
    "let": LET,
    "true": TRUE,
    "false": FALSE,
    "if": IF,
    "else": ELSE,
    "return": RETURN,
}

def lookup_ident(ident: str) -> TokenType:
    """Looks up an identifier to see if it is a keyword."""
    return keywords.get(ident, IDENT)
