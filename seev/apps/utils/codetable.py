"""
Utility for getting code translations
"""

CtGenMappings = {
    'BO': 'Boolean',
    'STR': 'String',
    'QTY': 'Quantity',
    'ENUM': 'Enumeration',
    '0': 'No Discount',
    '5': '5% Discount',
    '10': '10% Discount',
    '15': '15% Discount',
    '20': '20% Discount',
    '25': '25% Discount',
    '30': '30% Discount',
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
