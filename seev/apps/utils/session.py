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
