from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.go_cat_home, name='go_cat_home'),
    re_path(r'^add-pr/$', views.add_ctg_pr, name='add_ctg_pr'),
    re_path(r'^rm-pr/$', views.rm_ctg_pr, name='rm_ctg_pr'),
    re_path(r'^pr-config/$', views.go_pr_config, name='go_pr_config'),
]
