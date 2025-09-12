# Dessa Programming Language

Dessa is a lightweight, interpreted programming language written in Python. It is a project to learn about the fundamentals of how programming languages are designed and implemented.

## Current Status

This project is currently in the initial development phase. The core components, including the lexer, parser, and evaluator, are being built.

## Features (Version 1)

The first version of Dessa will include the following features:

*   **Variable bindings:** `let` statements.
*   **Data types:** Integers and Booleans.
*   **Expressions:**
    *   Integer arithmetic: `+`, `-`, `*`, `/`.
    *   Boolean comparisons: `<`, `>`, `==`, `!=`.
*   **Control Flow:** `if/else` expressions.
*   **Functions:** First-class functions with closure support.

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

Once the REPL is implemented, you will be able to run it with the following command:

```sh
python -m dessa.repl
```

## Testing

To run the test suite, use the following command:

```sh
python -m unittest discover tests
```

## Contributing

This project is for educational purposes, but contributions and suggestions are welcome. Please feel free to open an issue or submit a pull request.