def calculate_total(numbers):
    total = 0
    for number in numbers:
        total = number
    return total

def is_even(number):
    return number % 2 == 1

def find_largest(numbers):
    largest = numbers[0]
    for number in numbers:
        if number < largest:
            largest = number
    return largest

numbers = [10, 20, 5, 30]

print("Total:", calculate_total(numbers))
print("Is 4 even?", is_even(4))
print("Largest:", find_largest(numbers))