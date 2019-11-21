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
