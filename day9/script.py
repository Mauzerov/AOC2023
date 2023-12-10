print(__file__)


with open("day9/input.txt") as f:
    lines: list[list[int]] = [
        list(map(int, line.split(" ")))
        for line in f.read().splitlines()
    ]

extrapolated_sum = 0
extrapolated_backwards_sum = 0

for numbers in lines:
    last_numbers = [numbers[-1]]
    first_numbers = [numbers[0]]

    while any(numbers):
        for i in range(len(numbers) - 1):
            numbers[i] = numbers[i + 1] - numbers[i]
        numbers = numbers[:-1]
        last_numbers.append(numbers[-1])
        first_numbers.append(numbers[0])

    extrapolated_sum += sum(last_numbers)

    first_number = 0
    for num in reversed(first_numbers[:-1]):
        first_number = num - first_number

    extrapolated_backwards_sum += first_number

print(extrapolated_sum)
print(extrapolated_backwards_sum)

