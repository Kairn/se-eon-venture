from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.go_cat_home, name='go_cat_home'),
    re_path(r'^add-pr/$', views.add_ctg_pr, name='add_ctg_pr'),
    re_path(r'^rm-pr/$', views.rm_ctg_pr, name='rm_ctg_pr'),
    re_path(r'^pr-config/$', views.go_pr_config, name='go_pr_config'),
    re_path(r'^pr-chg/$', views.chg_pr_name, name='chg_pr_name'),
    re_path(r'^add-spec/$', views.add_ctg_spec, name='add_ctg_spec'),
    re_path(r'^add-fet/$', views.add_ctg_fet, name='add_ctg_fet'),
    re_path(r'^rm-spec/$', views.rm_ctg_spec, name='rm_ctg_spec'),
    re_path(r'^rm-fet/$', views.rm_ctg_fet, name='rm_ctg_fet'),
    re_path(r'^fet-config/$', views.go_fet_config, name='go_fet_config'),
    re_path(r'^fet-chg/$', views.chg_fet, name='chg_fet'),
    re_path(r'^sp-config/$', views.go_spec_config, name='go_spec_config'),
    re_path(r'^sp-chg/$', views.chg_spec, name='chg_spec'),
    re_path(r'^add-val/$', views.add_ctg_val, name='add_ctg_val'),
    re_path(r'^save-res/$', views.save_ctg_res, name='save_ctg_res'),
]
