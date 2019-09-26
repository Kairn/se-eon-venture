"""
Providing data generation utilities
"""

import string
import random
import hashlib

from seev.apps.core.models import UnoClient


def getAdminCredentials():
    """
    Get admin username and password hashes
    """
    credentials = [
        '6a211a6f0e1f095db8c26a17230505b91a685685a8d93413055b5689',
        'dbb0cd2ec71eb16be7340abf483cc9f999427aadafb79ead49fe0115'
    ]

    return credentials


def getCpAdminId():
    """
    Get cpadmin ID
    """
    return '-777'


def getClientStates(key):
    if (key == 'Approved' or key == 'AP'):
        return 'Approved'
    elif (key == 'Pending' or key == 'PE'):
        return 'Pending'
    elif (key == 'Denied' or key == 'DE'):
        return 'Denied'
    elif (key == 'Revoked' or key == 'RV'):
        return 'Revoked'


def getRandomSalt(length):
    """
    Generate a random salt of specified length
    """
    if length is not None and length > 0:
        pass
    else:
        length = 4

    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


def getSha384Hash(message):
    """
    Get SHA-384 digest of a message
    """
    if message is not None:
        _m = message.encode('U8')

        return hashlib.sha384(_m).hexdigest()
    else:
        return ''


def getSha224Hash(message):
    """
    Get SHA-224 digest of a message
    """
    if message is not None:
        _m = message.encode('U8')

        return hashlib.sha224(_m).hexdigest()
    else:
        return ''


def getFullCatalogCode(code, client=None, client_id=None):
    if not code or (not client and not client_id):
        return ''

    try:
        if not client:
            client = UnoClient.objects.get(client_id=client_id)

        return (str(client.ctg_name) + '_' + str(code)).upper()
    except Exception:
        return ''


def getDefCatalogCode(fullCode):
    if not fullCode:
        return ''
    else:
        return '_'.join(fullCode.split('_')[1:])
