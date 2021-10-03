import sys
from adapters.FileReaderAdapter import read_file
from adapters.OutputAdapter import format_output
from controllers.handlers.AuthorizerHandler import handle_input


def main():
    input_data = read_file(sys.stdin)
    print(format_output(handle_input(input_data)))


if __name__ == "__main__":
    main()
