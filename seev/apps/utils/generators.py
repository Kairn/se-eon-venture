# Providing data generation utilities

import string
import random
import hashlib


# Generate a random salt of specified length
def getRandomSalt(length):
    if length is not None and length > 0:
        pass
    else:
        length = 4

    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))


# Get SHA-384 digest of a message
def getSha384Hash(message):
    if message is not None:
        _m = message.encode('U8')

        return hashlib.sha384(_m).hexdigest()
    else:
        return ''
