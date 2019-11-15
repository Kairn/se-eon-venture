"""
Providing data generation utilities
"""

import os
import string
import random
import hashlib

from seev.apps.core.models import UnoClient
from seev.apps.utils.codetable import getGeneralTranslation


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


def generateOrderMeta(order):
    try:
        if not order:
            return None

        order_meta = {}
        order_meta['order_number'] = str(order.order_number).replace('-', '')
        order_meta['order_name'] = order.order_name
        order_meta['order_dis_mrc'] = order.opportunity.discount_mrc
        order_meta['order_dis_nrc'] = order.opportunity.discount_nrc
        order_meta['order_status'] = getGeneralTranslation(order.status)
        order_meta['client_name'] = order.client.entity_name
        order_meta['client_email'] = order.client.contact_email
        order_meta['client_phone'] = order.client.contact_phone
        order_meta['customer_name'] = order.customer.customer_name
        order_meta['opportunity_number'] = str(
            order.opportunity.opportunity_number).replace('-', '')

        return order_meta
    except Exception:
        return None


def generateOrderData(order):
    try:
        if not order:
            return None

        ordData = {}
        ordData['ordId'] = order.order_instance_id
        ordData['ordNumber'] = str(order.order_number).replace('-', '')
        ordData['ordName'] = order.order_name
        ordData['oppoNum'] = str(
            order.opportunity.opportunity_number).replace('-', '')
        ordData['customer'] = order.customer.customer_name
        ordData['business'] = order.client.entity_name
        ordData['ordStatus'] = getGeneralTranslation(order.status)
        ordData['ordCreDate'] = order.creation_time

        return ordData
    except Exception:
        return None


def getGoogleMapApiSource():
    apiKey = os.environ['SEEV_GOOG_KEY']
    callBack = 'initGoogleSearchMap'
    template = 'https://maps.googleapis.com/maps/api/js?key={0}&libraries=places&callback={1}'

    return template.format(apiKey, callBack)
