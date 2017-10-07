#!python
# Basic Syntax
# Write a program that asks the user for a number (integer only)
# and prints the sum of its digits

def sum_digits(integer_only):
    string = str(integer_only)
    numbers = [int(x) for x in string]
    return sum(numbers)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--number', required=True)
    args = parser.parse_args()
    print(sum_digits(int(args.number)))
