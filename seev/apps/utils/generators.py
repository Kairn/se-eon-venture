# Providing data generation utilities

import string
import random
import hashlib


# Get admin username and password hashes
def getAdminCredentials():
    credentials = [
        '6a211a6f0e1f095db8c26a17230505b91a685685a8d93413055b5689',
        'dbb0cd2ec71eb16be7340abf483cc9f999427aadafb79ead49fe0115'
    ]

    return credentials


# Get cpadmin ID
def getCpAdminId():
    return '-777'


# Generate a random salt of specified length
def getRandomSalt(length):
    if length is not None and length > 0:
        pass
    else:
        length = 4

    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


# Get SHA-384 digest of a message
def getSha384Hash(message):
    if message is not None:
        _m = message.encode('U8')

        return hashlib.sha384(_m).hexdigest()
    else:
        return ''


# Get SHA-224 digest of a message
def getSha224Hash(message):
    if message is not None:
        _m = message.encode('U8')

        return hashlib.sha224(_m).hexdigest()
    else:
        return ''
