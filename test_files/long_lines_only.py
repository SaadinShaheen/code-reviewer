def exactly_79_characters():
    """This function's body line is exactly 79 characters (not flagged)."""
    x = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    return x

def exactly_80_characters():
    """This function's body line is exactly 80 characters (flagged)."""
    x = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    return x

def very_long_line():
    """This function has one very long line (flagged)."""
    message = 'word word word word word word word word word word word word word word word word word word word word word word word word word end'
    return message