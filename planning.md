# Plan for building the "dessa" programming language

The language will be built in Python using a phased, test-driven approach.

## Phase 0: Project Setup & Core Data Structures
*   **Goal:** Establish the project foundation.
*   **Actions:**
    *   Create the directory structure: a `dessa/` source directory for the language components and a `tests/` directory for unit tests.
    *   Define core data structures that will be used throughout the project, such as the `Token` class (for the lexer) and base classes for the Abstract Syntax Tree (AST) nodes (for the parser).

## Phase 1: The Lexer (or Tokenizer)
*   **Purpose:** To take raw source code and break it into a series of "tokens".
*   **Example:** `let x = 5;` -> `[LET, IDENTIFIER("x"), ASSIGN, INTEGER(5), SEMICOLON]`.
*   **Testing:** Write unit tests to verify that various input strings are correctly tokenized.

## Phase 2: The Parser
*   **Purpose:** To take the token stream and build an Abstract Syntax Tree (AST), which gives the code its structure.
*   **Testing:** Write unit tests to ensure the parser correctly builds the AST for valid sequences of tokens.

## Phase 3: The Evaluator (or Interpreter)
*   **Purpose:** To walk the AST and execute the code to produce a result.
*   **Testing:** Write unit tests to confirm that various ASTs evaluate to the correct results (e.g., `1 + 2` evaluates to `3`).

## Phase 4: The REPL (Read-Eval-Print Loop)
*   **Purpose:** To create the interactive command-line interface for "dessa". It will tie all the previous components together.
*   **Testing:** Manual testing will be the primary method for the REPL.

## Core Feature Set (Version 1)
To keep the initial scope focused, the first version of "dessa" will include:
*   **Variable bindings:** `let` statements.
*   **Data types:** Integers and Booleans.
*   **Expressions:**
    *   Integer arithmetic: `+`, `-`, `*`, `/`.
    *   Boolean comparisons: `<`, `>`, `==`, `!=`.
*   **Control Flow:** `if/else` expressions. Block statements will be enclosed in curly braces `{ ... }`.

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
