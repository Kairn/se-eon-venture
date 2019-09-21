"""
View logic used in catalog app
"""

import traceback

from django.db import transaction
from django.shortcuts import render, redirect, reverse

from seev.apps.core.models import UnoClient

from .models import CtgProduct, CtgFeature, CtgSpecification, CtgValue, CtgRestriction, CtgPrice
from .forms import AddPrForm


# Also the add product UI
def go_cat_home(request, context=None):
    try:
        if not context:
            context = {}

        client = UnoClient.objects.get(client_id=request.session['id'])
        context['client'] = client
        context['addPrForm'] = AddPrForm()

        return render(request, 'catalog/index.html', context=context)
    except Exception:
        if request and hasattr(request, 'session'):
            request.session.clear()
        return redirect('go_login')


@transaction.atomic
def add_ctg_pr(request, context=None):
    if request.method == 'POST':
        pass
    else:
        return redirect('go_cat_home')
