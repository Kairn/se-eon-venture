"""
Manage session related shortcut functions
"""

from seev.apps.utils.generators import *


def store_context_in_session(request, context):
    if request and hasattr(request, 'session'):
        request.session['context'] = context
    else:
        return


def get_context_in_session(request):
    if request and hasattr(request, 'session'):
        return request.session.pop('context', None)
    else:
        return None


def load_ord_meta_to_context(request, context):
    if not request:
        return {}

    if not context:
        context = {}

    if hasattr(request, 'session') and 'order_meta' in request.session and request.session['order_meta']:
        context['ordMeta'] = request.session['order_meta']
        context['data_on'] = request.session['order_meta']['on']
        context['data_os'] = request.session['order_meta']['os']
        return context
    else:
        return {}


def save_ord_meta_to_session(request, meta):
    if not request or not meta:
        return

    if hasattr(request, 'session'):
        request.session['order_meta'] = meta
    else:
        return


def clear_ord_meta(request):
    if request and hasattr(request, 'session') and 'order_meta' in request.session:
        del request.session['order_meta']
    else:
        return


def refreshOrdSessionData(order, request):
    if not order or not request:
        return
    else:
        meta = generateOrderMeta(order)
        save_ord_meta_to_session(request, meta)


def getOrCreateSvcError(request, svcId):
    if not request or not hasattr(request, 'session') or not svcId:
        return None

    if 'errorMap' in request.session:
        if svcId in request.session['errorMap']:
            return request.session['errorMap'][svcId]
        else:
            return []
    else:
        request.session['errorMap'] = {}
        return []


def saveErrorInMap(request, svcId, errorList):
    if not request or not hasattr(request, 'session') or not svcId or errorList == None:
        return

    if 'errorMap' in request.session:
        request.session['errorMap'][svcId] = errorList
    else:
        request.session['errorMap'] = {}
        request.session['errorMap'][svcId] = errorList


def getUserAndOrderId(request):
    if request and hasattr(request, 'session'):
        idArray = []
        userId = None
        orderId = None

        if 'id' in request.session:
            userId = request.session['id']
        if 'order_meta' in request.session:
            order = getOrderByNumber(
                request.session['order_meta']['order_number'])
            orderId = order.order_instance_id if order else None

        idArray.append(userId)
        idArray.append(orderId)
        return idArray
    else:
        return [None, None]
