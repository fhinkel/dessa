import sys
from dessa.lexer import Lexer
from dessa.parser import Parser
from dessa.evaluator import eval
from dessa.object import Object
from dessa.environment import Environment

PROMPT = ">> "


def main():
    """Starts the REPL."""
    env = Environment()
    while True:
        sys.stdout.write(PROMPT)
        sys.stdout.flush()
        line = sys.stdin.readline()
        if not line:
            break
        lexer = Lexer(line)
        parser = Parser(lexer)
        program = parser.parse_program()
        if parser.errors:
            for error in parser.errors:
                sys.stderr.write(f"\t{error}\n")
            continue
        evaluated = eval(program, env)
        if evaluated is not None:
            sys.stdout.write(evaluated.inspect())
            sys.stdout.write("\n")


if __name__ == "__main__":
    main()
