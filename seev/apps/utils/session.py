"""
Manage session related shortcut functions
"""


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
