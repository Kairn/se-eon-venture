from django.shortcuts import render, redirect

from .forms import LoginForm, PasswordResetForm, RegisterForm

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
    if request.method == 'GET':
        loginForm = LoginForm()
        psrForm = PasswordResetForm()
        context['loginForm'] = loginForm
        context['psrForm'] = psrForm

    return render(request, 'core/login.html', context=context)


def auth_login(request):
    if request.method == 'POST':
        return redirect('go_landing')
    else:
        return redirect('go_login')


def auth_password_reset(request):
    if request.method == 'POST':
        return redirect('go_landing')
    else:
        return redirect('go_login')


def go_register(request):
    context = {}
    if request.method == 'GET':
        registerForm = RegisterForm()
        context['registerForm'] = registerForm

    return render(request, 'core/register.html', context=context)


def do_register(request):
    if request.method == 'POST':
        return redirect('go_landing')
    else:
        return redirect('go_register')
