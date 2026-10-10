def calculate_total(numbers):
    """Return the sum of all numbers in the list."""
    total = 0
    for number in numbers:
        total += number
    return total
 
def is_even(number):
    """Return True if the number is even."""
    return number % 2 == 0
 
def find_largest(numbers):
    """Return the largest number, or None for an empty list."""
    if not numbers:
        return None
    largest = numbers[0]
    for number in numbers[1:]:
        if number > largest:
            largest = number
    return largest

def average(numbers):
    """Return the average of the numbers, or 0 for an empty list."""
    if not numbers:
        return 0
    return calculate_total(numbers) / len(numbers)

def count_vowels(text):
    """Return how many vowels the text contains."""
    count = 0
    for char in text.lower():
        if char in "aeiou":
            count += 1
    return count

numbers = [10, 20, 5, 30]
print("Total:", calculate_total(numbers))
print("Is 4 even?", is_even(4))
print("Largest:", find_largest(numbers))
print("Average:", average(numbers))
print("Vowels:", count_vowels("Code Reviewer"))