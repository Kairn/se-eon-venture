from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.go_landing, name='go_landing'),
    re_path(r'^login/$', views.go_login, name='go_login'),
    re_path(r'^auth-login/$', views.auth_login, name='auth_login'),
    re_path(r'^auth-psr/$', views.auth_password_reset,
            name='auth_password_reset'),
    re_path(r'^register/$', views.go_register, name='go_register'),
    re_path(r'^do-reg/$', views.do_register, name='do_register'),
    re_path(r'^cpadmin/$', views.go_admin, name='go_admin'),
    re_path(r'^logout/$', views.go_logout, name='go_logout'),
    re_path(r'^success/$', views.go_success, name='go_success'),
    re_path(r'^error/$', views.go_error, name='go_error'),
    re_path(r'^do-approve/$', views.do_approve, name='do_approve'),
    re_path(r'^client/$', views.go_client, name='go_client'),
    re_path(r'^enroll/$', views.do_enroll, name='do_enroll'),
    re_path(r'^do-oppo/$', views.do_oppo, name='do_oppo'),
    re_path(r'^records/$', views.go_records, name='go_records'),
    re_path(r'^can-oppo/$', views.can_oppo, name='can_oppo'),
    re_path(r'^bad/$', views.go_bad_view, name='go_bad_view'),
]
