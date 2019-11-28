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
        'enroll_error': 'Enrollment Failure',
        'enroll_error_message': 'An error occurred during customer enrollment. Please contact a system administrator.',
        'enroll_success': 'A new customer has been successfully enrolled. We look forward to taking their orders.',
        'oppo_error': 'Acknowledgment Failed',
        'oppo_error_message': 'Sorry, we are unable to create this opportunity. Please contact a system administrator.',
        'oppo_can_error': 'Annulment Failure',
        'oppo_can_message': 'Internal error occurred for the request opportunity. Please contact a system administrator.',
        'catalog_error': 'Business Catalog Error',
        'catalog_error_message': 'We have encountered an error while retrieving data from the current client partner. This might be caused by incomplete catalog definition. Please contact your business client.',
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


def getNewOppoMessage(oppo_number):
    if not oppo_number:
        return ''

    oppo_number = str(oppo_number).replace('-', '')

    return 'Opportunity number <span class="imp-num">{0}</span> has been created successfully. Please share this number with the customer.'.format(oppo_number)
