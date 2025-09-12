# Plan for building the "dessa" programming language

The language will be built in Python using a phased, test-driven approach.

## Phase 0: Project Setup & Core Data Structures - Detailed Plan

*   **Goal:** To establish a solid foundation for the project by creating the necessary directory structure and defining the core data structures that will be used throughout the compiler/interpreter.

### 0.1. Directory and File Structure

*   **Task:** Create the following directory and file structure. This organizes the project into source code (`dessa`), tests (`tests`), and project-level configuration.

```
/
├── dessa/
│   ├── __init__.py
│   ├── token.py
│   ├── ast.py
│   └── lexer.py
├── tests/
│   ├── __init__.py
│   └── test_lexer.py
├── planning.md
└── readme.md
```

*   **Action:**
    *   Run `mkdir -p dessa tests` to create the main directories.
    *   Run `touch dessa/__init__.py tests/__init__.py` to create the package markers.
    *   Run `touch dessa/token.py dessa/ast.py dessa/lexer.py tests/test_lexer.py` to create the initial empty files.

### 0.2. Core Data Structure: The `Token`

*   **File:** `dessa/token.py`
*   **Purpose:** The `Token` is the smallest unit of meaning in the code. The lexer will turn a string of source code into a stream of these tokens.
*   **Task:** Define the `Token` data structure and the supported token types.
*   **Implementation:**
    *   Use a `dataclass` for a concise and readable `Token` definition.
    *   Define string constants for each `TokenType` to avoid errors from typos.

*   **Code Skeleton (`dessa/token.py`):**
    ```python
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

    ```

### 0.3. Core Data Structure: The Abstract Syntax Tree (AST)

*   **File:** `dessa/ast.py`
*   **Purpose:** The AST is a tree representation of the code's structure, created by the parser from the token stream. It's what the evaluator will execute.
*   **Task:** Define the base interfaces for all AST nodes.
*   **Implementation:**
    *   Every node in the AST will be a class that inherits from a base `Node`.
    *   There will be two main sub-types of nodes: `Statement` and `Expression`.
    *   Each node class will be responsible for holding its relevant information (e.g., an `Identifier` node will hold the token and its string value).

*   **Code Skeleton (`dessa/ast.py`):**
    ```python
    from abc import ABC, abstractmethod
    from dessa.token import Token

    class Node(ABC):
        """The base class for all AST nodes."""
        @abstractmethod
        def token_literal(self) -> str:
            """Returns the literal value of the token associated with the node."""
            pass

        def __str__(self) -> str:
            return f"AST Node <{self.__class__.__name__}>"


    class Statement(Node):
        """A statement is a piece of code that does not produce a value."""
        pass


    class Expression(Node):
        """An expression is a piece of code that produces a value."""
        pass


    class Program(Node):
        """The root node of every AST our parser produces."""
        def __init__(self) -> None:
            self.statements: list[Statement] = []

        def token_literal(self) -> str:
            if self.statements:
                return self.statements[0].token_literal()
            else:
                return ""

        def __str__(self) -> str:
            return "".join(str(s) for s in self.statements)

    ```

### 0.4. Initial Test File Setup

*   **File:** `tests/test_lexer.py`
*   **Purpose:** To prepare for the test-driven development of the lexer in Phase 1.
*   **Task:** Create an initial test file with a placeholder test case.
*   **Code Skeleton (`tests/test_lexer.py`):**
    ```python
    import unittest
    from dessa.token import Token, TokenType

    class LexerTest(unittest.TestCase):
        def test_placeholder(self):
            self.assertEqual(1, 1)

    if __name__ == '__main__':
        unittest.main()
    ```

## Phase 1: The Lexer (or Tokenizer) - Detailed Plan for Intern

*   **Purpose:** To take raw source code and break it into a series of "tokens".

### 1.1. The Token Data Structure

*   **File:** `dessa/token.py`
*   **Task:** Define a `Token` class or a `dataclass` to represent a token. Each token should have the following attributes:
    *   `type` (str): The type of the token (e.g., "LET", "IDENTIFIER").
    *   `literal` (str): The actual text of the token (e.g., "let", "x").
    *   `line` (int): The line number where the token appears.
    *   `column` (int): The column number where the token appears.

### 1.2. Token Types

*   **File:** `dessa/token.py`
*   **Task:** Define constants for all the token types your lexer will produce. This avoids typos and makes the code more readable.

```python
# Example Token Types
LET = "LET"
IDENTIFIER = "IDENTIFIER"
ASSIGN = "="
INTEGER = "INTEGER"
SEMICOLON = ";"
# ... and so on
```

*   **Required Tokens for V1:**
    *   **Keywords:** `let`, `if`, `else`, `true`, `false`, `fn`, `return`
    *   **Identifiers:** `my_variable`, `x`, `y`, etc.
    *   **Literals:** Integers (e.g., `5`, `10`, `834`)
    *   **Operators:** `=`, `+`, `-`, `*`, `/`, `<`, `>`, `==`, `!=`
    *   **Delimiters:** `(`, `)`, `{`, `}`, `,`, `;`
    *   **Special:** `ILLEGAL` (for unknown characters), `EOF` (for End of File).

### 1.3. The Lexer Class

*   **File:** `dessa/lexer.py`
*   **Task:** Create a `Lexer` class.
*   **Structure:**
    *   The `__init__` method should take the source code string as input and initialize properties like `position`, `read_position`, and the current `char`.
    *   A `next_token()` method will be the main workhorse. It will read the input, identify the next token, and return a `Token` object.
    *   Helper methods like `_read_char()`, `_peek_char()`, `_read_identifier()`, `_read_number()`, and `_skip_whitespace()` will be necessary.

### 1.4. Implementation Steps

1.  **Start with single-character tokens:** In `next_token()`, use a `match` or `if/elif` statement to handle tokens like `+`, `-`, `(`, `)`, etc.
2.  **Handle multi-character tokens:** Add logic to peek ahead for tokens like `==` and `!=`.
3.  **Implement whitespace skipping:** The lexer should consume and ignore whitespace characters (spaces, tabs, newlines).
4.  **Implement `_read_identifier()`:** This helper will read a sequence of letters and underscores and look up if it's a keyword. If not, it's an `IDENTIFIER`.
5.  **Implement `_read_number()`:** This helper will read a sequence of digits and create an `INTEGER` token.
6.  **Handle `EOF` and `ILLEGAL`:** When the end of the input is reached, return an `EOF` token. If an unrecognized character is found, return an `ILLEGAL` token.

### 1.5. Testing (`tests/test_lexer.py`)

*   **Goal:** Write comprehensive unit tests to ensure the lexer works correctly.
*   **Test Cases:**
    *   **Simple tokens:** Test that single tokens like `+`, `=`, and `;` are tokenized correctly.
    *   **A simple statement:** `let x = 5;` -> `[LET, IDENTIFIER("x"), ASSIGN, INTEGER(5), SEMICOLON, EOF]`
    *   **A more complex statement:**
        ```
        let five = 5;
        let ten = 10;
        let add = fn(x, y) {
          x + y;
        };
        let result = add(five, ten);
        ```
    *   **Operators:** Test all arithmetic and comparison operators.
    *   **Error Handling:** Test with an illegal character (e.g., `@`) and ensure it produces an `ILLEGAL` token.

## Phase 2: The Parser
*   **Purpose:** To take the token stream and build an Abstract Syntax Tree (AST).
*   **Technique:** Implement a top-down recursive descent parser. A Pratt parser will be used to handle operator precedence.
*   **Error Handling:** Provide clear, informative error messages for syntax errors, including line and column numbers.
*   **Testing:** Write unit tests to ensure the parser correctly builds the AST for valid sequences of tokens and reports errors for invalid sequences.

## Phase 3: The Evaluator (or Interpreter)
*   **Purpose:** To walk the AST and execute the code.
*   **Core Components:**
    *   **Object System:** Create an internal object system to represent language values (e.g., `Integer`, `Boolean`).
    *   **Environment:** Implement an `Environment` object to manage variable bindings and scope.
*   **Error Handling:** Handle runtime errors such as type mismatches or undefined variables.
*   **Testing:** Write unit tests to confirm that various ASTs evaluate to the correct results.

## Phase 4: The REPL (Read-Eval-Print Loop)
*   **Purpose:** To create an interactive command-line interface for "dessa".
*   **Testing:** While manual testing is primary, implement automated tests to simulate user input and verify REPL output.

## Core Feature Set (Version 1)
To keep the initial scope focused, the first version of "dessa" will include:
*   **Variable bindings:** `let` statements.
*   **Data types:** Integers and Booleans.
*   **Expressions:**
    *   Integer arithmetic: `+`, `-`, `*`, `/`.
    *   Boolean comparisons: `<`, `>`, `==`, `!=`.
*   **Control Flow:** `if/else` expressions that return a value (e.g., `let result = if (x > 0) { 1 } else { -1 };`). Block statements will be enclosed in curly braces `{ ... }`.

## Future Features (Post-V1)

Once the core feature set is complete and tested, we can extend "dessa" with more powerful capabilities.

*   **Functions:**
    *   **First-class functions:** Treat functions as values that can be assigned to variables and passed to other functions.
    *   **Syntax:** Define function literals with the `fn` keyword, followed by parameters and a block statement body. Example: `let add = fn(x, y) { x + y; };`
    *   **Closures:** Ensure functions carry their enclosing environment with them.

*   **String Data Type:**
    *   **Syntax:** Support for double-quoted string literals. Example: `let name = "Dessa";`
    *   **Operations:** Plan for basic operations like concatenation.

*   **Array Data Type:**
    *   **Syntax:** Support for array literals with comma-separated values. Example: `let my_array = [1, "two", fn(x){x*x}];`
    *   **Operations:** Support for element access via index. Example: `my_array[0]`.

*   **Hash Map Data Type:**
    *   **Syntax:** Support for hash literals with key-value pairs. Example: `let my_hash = {"name": "Dessa", "age": 5};`
    *   **Operations:** Support for element access via key. Example: `my_hash["name"]`.