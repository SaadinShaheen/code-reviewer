def sum_all_but_last(items):
    """Return the sum of every item in the list."""
    total = 0
    for i in range(len(items) - 1):
        total += items[i]
    return total

def average(numbers):
    """Return the average of the numbers."""
    return sum(numbers) / len(numbers)

def add_item(item, items=[]):
    """Add an item to a new list and return the list."""
    items.append(item)
    return items

def first_negative(numbers):
    """Return the first negative number, or None."""
    for number in numbers:
        if number < 0:
            return number
        return None
    
def in_range(x):
    """Return True if x is between 1 and 10 inclusive."""
    return x > 1 and x < 10