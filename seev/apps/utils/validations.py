"""
Utility functions for data validation
"""

import re

# Regex patterns
EMAIL_PATTERN = r'^[^_\W][\w\.]*@\w+\.\w+$'
DOUBLE_DOTS_PATTERN = r'\.\.'
SPACE_PATTERN = r'\s'
DIGIT_PATTERN = r'\d'
NON_DIGIT_PATTERN = r'\D'
LOWER_CASE_PATTERN = r'[a-z]'
UPPER_CASE_PATTERN = r'[A-Z]'
SPECIAL_PATTERN = r'[\W_]'


# Simple validations
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


# Bulk request validations
def isValidRegisterRequest(post_data):
    try:
        if post_data is None:
            return False

        if isValidEmail(post_data['contact_email']) == False:
            return False

        if isValidEmail(post_data['recovery_email']) == False:
            return False

        if isValidPhone(post_data['contact_phone']) == False:
            return False

        if isValidUsername(post_data['username']) == False:
            return False

        if isValidPassword(post_data['password']) == False:
            return False

        if post_data['password'] != post_data['confirm_password']:
            return False

        return True
    except:
        return False
