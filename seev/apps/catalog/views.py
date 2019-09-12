"""
View logic used in catalog app
"""

import traceback

from django.db import transaction
from django.shortcuts import render, redirect, reverse

from seev.apps.core.models import UnoClient


def go_cat_home(request, context=None):
    try:
        if not context:
            context = {}

        client = UnoClient.objects.get(client_id=request.session['id'])
        context['client'] = client

        return render(request, 'catalog/index.html', context=context)
    except Exception:
        if request and hasattr(request, 'session'):
            request.session.clear()
        return redirect('go_login')
