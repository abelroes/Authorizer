import sys
from adapters.FileReaderAdapter import read_file


def main():
    input_data = read_file(sys.stdin)
    print(input_data)
    
    


if __name__ == "__main__":
    main()