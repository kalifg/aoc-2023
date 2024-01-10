import sys

sys.path.append('../shared')

from shared import input

digit_words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def get_digits(line):
    digits = [(char, idx) for idx, char in enumerate(line) if char.isdigit()]

    if not digits:
        return ()

    return digits[0], digits[-1]


def get_digit_words(line):
    # print(line)
    occurences = [t for t in [(word, line.find(word)) for word in digit_words] if t[1] > -1]

    if not occurences:
        return ()

    occurences = sorted(occurences, key=lambda t: t[1])

    reversed_line = line[::-1]
    # print(reversed_line)
    reversed_digit_words = [w[::-1] for w in digit_words]
    # print(reversed_digit_words)
    reveresed_occurences =  [(reversed_digit_word[::-1], len(line) - idx - len(reversed_digit_word)) for reversed_digit_word, idx in [(word, reversed_line.find(word)) for word in reversed_digit_words] if idx > -1]
    reveresed_occurences = sorted(reveresed_occurences, key=lambda t: -t[1])

    # print(occurences, reveresed_occurences)

    return occurences[0], reveresed_occurences[0]


def digit_word_to_int(digit_word):
    return digit_words.index(digit_word) + 1


def extract_num(line):
    words = get_digit_words(line)
    digits = get_digits(line)

    if not words:
        digit1 = digits[0][0]
        digit2 = digits[1][0]
    elif not digits:
        digit1 = digit_word_to_int(words[0][0])
        digit2 = digit_word_to_int(words[1][0])
    else:
        if words[0][1] < digits[0][1]:
            digit1 = digit_word_to_int(words[0][0])
        else:
            digit1 = digits[0][0]

        if words[1][1] > digits[1][1]:
            digit2 = digit_word_to_int(words[1][0])
        else:
            digit2 = digits[1][0]

    num = int(f'{digit1}{digit2}')
    print(f'{line}: {num}')
    # print()

    return num


def main(filename):
    lines = input.readfile(filename)
    sum = 0
    
    for line in lines:
        sum += extract_num(line)

    print()
    print(sum)


# 53332 too low
# 53340?
# 53347 too high

if __name__ == '__main__':
    main(sys.argv[1])