"""
View logic used in catalog app
"""

import traceback

from django.db import transaction
from django.shortcuts import render, redirect, reverse


def go_cat_home(request, context=None):
    if not context:
        context = {}

    return render(request, 'catalog/index.html', context=context)
