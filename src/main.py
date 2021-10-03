import sys
from adapters.FileReaderAdapter import read_file
from controllers.handlers.AuthorizerHandler import handle_input


def main():
    input_data = read_file(sys.stdin)
    handle_input(input_data)

if __name__ == "__main__":
    main()
