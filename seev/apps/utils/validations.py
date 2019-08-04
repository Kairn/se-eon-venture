# Utility functions for data validation

import re

EMAIL_PATTERN = r'^[^_\W][\w\.]*@\w+\.\w+$'
DOUBLE_DOTS_PATTERN = r'\.\.'
SPACE_PATTERN = r'\s'
DIGIT_PATTERN = r'\d'
NON_DIGIT_PATTERN = r'\D'
LOWER_CASE_PATTERN = r'[a-z]'
UPPER_CASE_PATTERN = r'[A-Z]'
SPECIAL_PATTERN = r'[\W_]'


def isValidEmail(input):
    input = input.strip()

    if re.search(EMAIL_PATTERN, input) == None:
        return False

    if re.search(DOUBLE_DOTS_PATTERN, input) != None:
        return False

    return True


def isValidPassword(input):
    input = input.strip()

    if len(input) < 8:
        return False

    if re.search(LOWER_CASE_PATTERN, input) == None:
        return False

    if re.search(UPPER_CASE_PATTERN, input) == None:
        return False

    if re.search(DIGIT_PATTERN, input) == None:
        return False

    if re.search(SPECIAL_PATTERN, input) == None:
        return False

    if re.search(SPACE_PATTERN, input) != None:
        return False

    return True


def isValidUsername(input):
    input = input.strip()

    if len(input) < 6:
        return False

    if re.search(SPACE_PATTERN, input) != None:
        return False

    return True


def isValidPhone(input):
    input = input.strip()

    if len(input) != 10:
        return False

    if re.search(NON_DIGIT_PATTERN, input) != None:
        return False

    return True
