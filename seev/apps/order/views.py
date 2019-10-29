"""
View logic used in catalog app
"""

import traceback

from django.db import transaction
from django.shortcuts import render, redirect, reverse

from seev.apps.utils.generators import (getFullCatalogCode, getDefCatalogCode)
from seev.apps.utils.codetable import getGeneralTranslation
from seev.apps.utils.messages import get_app_message, addSnackDataToContext
from seev.apps.utils.session import store_context_in_session, get_context_in_session

from seev.apps.core.models import UnoClient

from .models import *
from .forms import *


def go_ord_home(request, context=None):
    context = get_context_in_session(request)

    if not context:
        context = {}

    return render(request, 'order/index.html', context=context)


def find_oppo_by_num(request, context=None):
    if request.method == 'POST':
        try:
            oppoNumber = request.POST['opportunity-number']

            opportunity = UnoOpportunity.objects.get(
                opportunity_number=oppoNumber)
            if not opportunity.active or opportunity.deal_count >= opportunity.deal_limit:
                raise AssertionError

            # Fill opportunity details
            oppoData = {}

            context = {}
            context['oppoData'] = oppoData

            return render(request, 'order/index.html', context=context)
        except AssertionError:
            store_context_in_session(request, addSnackDataToContext(
                context, 'Opportunity has expired'))
            return redirect('go_ord_home')
        except Exception:
            traceback.print_exc()
            store_context_in_session(request, addSnackDataToContext(
                context, 'Opportunity not found'))
            return redirect('go_ord_home')
    else:
        return redirect('go_ord_home')
