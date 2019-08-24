"""
File for providing static messages or data
"""


def get_app_message(key):
    all_messages = {
        'register_success': 'We will be working hard to process your request.',
        'register_error': 'Invalid Data',
        'register_error_message': 'Sorry, we are unable to process your request. Please make sure you fill out all required fields and try again.',
        'approval_error': 'Management Error',
        'approval_error_message': 'There is an issue with your approval request. Please contact a system administrator.',
        '': '',
    }

    message = all_messages[key]

    if message is None or message == '':
        return 'Message not found'
    else:
        return message


def addSnackDataToContext(context, message):
    if context is None:
        context = {}

    if (message == 'ERR01'):
        context['snack_data'] = 'Internal server failure'
    elif (message == 'ERR02'):
        pass
    else:
        context['snack_data'] = message

    return context
