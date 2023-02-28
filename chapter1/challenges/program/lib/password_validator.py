# == INSTRUCTIONS ==
#
# Purpose: Validate a password
# Parameters: one, a string
# Rules:
#   - It must be longer than 7 characters (8 is fine)
#   - It must contain at least one of the following special characters: `!`, `@`,
#     `$`, `%` or `&`
# Returns: a boolean (True if valid, False otherwise)
# Example:
#   Call:    is_valid("1234567")
#   Returns: False
#   Call:    is_valid("12345678")
#   Returns: False
#   Call:    is_valid("12345!78")
#   Returns: True

# == YOUR CODE ==

import re
def is_valid(password):
    if len(password) < 7:
        return False
    elif re.search('[0-9]',password) is None:
        return False
    elif re.search('[A-Z]',password) is None:
        return False
    elif re.search('!@$%&!@$',password) is None:
        return False
    else:
        return True
