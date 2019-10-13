"""
Utility for getting code translations
"""

CtGenMappings = {
    'BO': 'Boolean',
    'STR': 'String',
    'QTY': 'Quantity',
    'ENUM': 'Enumeration',
}

CtSpecMappings = {
    '': '',
}


def getGeneralTranslation(code):
    if not code:
        return ''

    result = ''

    try:
        result = CtGenMappings[code]
    except Exception:
        result = ''

    return result


def getSpecificTranslation(code):
    if not code:
        return ''

    result = ''

    try:
        result = CtSpecMappings[code]
    except Exception:
        result = ''

    return result
