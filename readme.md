# Dessa Programming Language

Dessa is a lightweight, interpreted programming language written in Python. It is a project to learn about the fundamentals of how programming languages are designed and implemented.

## Current Status

This project is currently in the initial development phase. The core components, including the lexer, parser, and evaluator, are being built.

## Features

Dessa is a simple, dynamically-typed programming language that supports the following features:

*   **Variable Bindings:** Use the `let` keyword to bind values to names.
    ```
    let x = 5;
    let y = x * 2;
    ```

*   **Data Types:** Integers and booleans are the core data types.
    ```
    let is_active = true;
    let count = 10;
    ```

*   **Expressions:** Full support for arithmetic and boolean expressions with operator precedence.
    *   **Arithmetic:** `+`, `-`, `*`, `/`
    *   **Comparison:** `<`, `>`, `==`, `!=`
    *   **Prefix Operators:** `!` (negation), `-` (negative)

*   **Conditional Logic:** Use `if/else` expressions to control the flow of your code. `if` is an expression and produces a value.
    ```
    let result = if (x > y) { x } else { y };
    ```

*   **First-Class Functions and Closures:** Functions are first-class citizens. They can be assigned to variables, passed as arguments, and returned from other functions. They also support closures, capturing the environment in which they were created.
    ```
    let add = fn(x, y) {
      return x + y;
    };

    let newAdder = fn(x) {
      fn(y) { x + y };
    };
    let addTwo = newAdder(2);
    addTwo(3); // returns 5
    ```

## Future Features

The following features are planned for future versions:

*   **String Data Type**
*   **Array Data Type**
*   **Hash Map Data Type**

## Getting Started

To get started with the development of Dessa, you will need Python 3.10 or later and `uv`.

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd dessa
    ```

2.  **Create and activate the virtual environment:**
    ```sh
    uv venv
    source .venv/bin/activate
    ```

## Usage

You can start the interactive REPL (Read-Eval-Print Loop) by running the `main.py` script:

```sh
python3 main.py
```

This will launch a prompt where you can enter and execute Dessa code.

## Testing

To run the test suite, use the following command:

```sh
python -m unittest discover tests
```

## Contributing

This project is for educational purposes, but contributions and suggestions are welcome. Please feel free to open an issue or submit a pull request.