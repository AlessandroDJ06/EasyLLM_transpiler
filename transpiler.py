import os
from tokenizer.tokenizer import find_modules
from parser.parser import parse_modules

def main():
    test_file = "test.elm"

    if not os.path.isfile(test_file):
        print("File not found")
        return

    with open(test_file, "r", encoding="utf-8") as file:
        source = file.read()

    found_modules = find_modules(source)
    generated_code = parse_modules(found_modules)
    with open("DEBUG_OUTPUT.py", "w", encoding="utf-8") as debug_file:
        debug_file.write(generated_code)

    exec(generated_code)

if __name__ == "__main__":
    main()



