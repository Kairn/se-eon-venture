from django.shortcuts import render

# Create your views here.


def go_landing(request):
    context = {}
    return render(request, 'core/index.html', context=context)
