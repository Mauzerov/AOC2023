print(__file__)

with open("day1/input.txt", "r") as f:
    lines = f.readlines()

    for i, line in enumerate(lines):
        number = ''
        last_digit = ''
        for char in line:
            if not number and char.isdigit():
                number += char
            if char.isdigit():
                last_digit = char
        lines[i] = number + last_digit

    print(sum(map(int, lines)))

with open("day1/input.txt", "r") as f:
    lines = f.readlines()

    digits = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }

    for index, line in enumerate(lines):
        number = ''
        last_digit = ''
        for i in range(len(line)):
            if line[i].isdigit() and not number:
                number += line[i]
                last_digit = line[i]
            elif line[i].isdigit():
                last_digit = line[i]
            else:
                for j in range(i + 3, len(line)):
                    if line[i:j] in digits:
                        if not number:
                            number += digits[line[i:j]]
                        last_digit = digits[line[i:j]]
                        break
        lines[index] = number + last_digit

    print(sum(map(int, lines)))
