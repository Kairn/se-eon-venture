from django.shortcuts import render

# Create your views here.


def go_landing(request):
    request.session.set_test_cookie()

    context = {}
    return render(request, 'core/index.html', context=context)


def go_login(request):
    if request.session.test_cookie_worked():
        print('Django session is working')
        request.session.delete_test_cookie()

    context = {}
    return render(request, 'core/login.html', context=context)
