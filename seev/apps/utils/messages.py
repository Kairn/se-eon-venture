# File for providing static messages or data


def get_app_message(key):
    all_messages = {
        'register_success': 'We will be working hard to process your request.',
        'register_error': 'Invalid Data',
        'register_error_message': 'Sorry, we are unable to process your request. Please make sure you fill out all required fields and try again.',
        '': '',
    }

    message = all_messages[key]

    if message is None or message == '':
        return 'Message not found'
    else:
        return message
