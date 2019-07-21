from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.go_landing, name='go_landing'),
    re_path(r'^login/$', views.go_login, name='go_login'),
    re_path(r'^auth-login/$', views.auth_login, name='auth_login'),
    re_path(r'^auth-psr/$', views.auth_password_reset,
            name='auth_password_reset'),
]
