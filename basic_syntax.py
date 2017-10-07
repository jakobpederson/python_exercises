#!python
# Basic Syntax
# Write a program that asks the user for a number (integer only)
# and prints the sum of its digits
from collections import Counter

def sum_digits(integer_only):
    string = str(integer_only)
    numbers = [int(x) for x in string]
    return sum(numbers)


"""
Write program that takes a file name as command line argument,
count how many times each word appears in the file and prints
the word that appears the most (and its relevant count)
"""
def most_common_word(file_path):
    with open(file_path, 'r') as f:
        data = f.readlines()
    result = data[0].split()
    c = Counter(result)
    if c.most_common(1):
        return c.most_common(1)[0]
    return "No words"

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--number', required=True)
    args = parser.parse_args()
    print(sum_digits(int(args.number)))
