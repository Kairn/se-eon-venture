from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.go_ord_home, name='go_ord_home'),
    re_path(r'^find-oppo/$', views.find_oppo_by_num, name='find_oppo_by_num'),
    re_path(r'^create-order/$', views.create_order, name='create_order'),
    re_path(r'^config-home/$', views.go_ord_config_home,
            name='go_ord_config_home'),
    re_path(r'^find-ord/$', views.find_ord_by_num, name='find_ord_by_num'),
]
