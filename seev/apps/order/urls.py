from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.go_ord_home, name='go_ord_home'),
    re_path(r'^find-oppo/$', views.find_oppo_by_num, name='find_oppo_by_num'),
]
