from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.go_ord_home, name='go_ord_home'),
    re_path(r'^find-oppo/$', views.find_oppo_by_num, name='find_oppo_by_num'),
    re_path(r'^create-order/$', views.create_order, name='create_order'),
    re_path(r'^config-home/$', views.go_ord_config_home,
            name='go_ord_config_home'),
    re_path(r'^find-ord/$', views.find_ord_by_num, name='find_ord_by_num'),
    re_path(r'^auth-ord/$', views.auth_access_order, name='auth_access_order'),
    re_path(r'^exit-ord/$', views.exit_order, name='exit_order'),
    re_path(r'^config-site/$', views.go_site_config, name='go_site_config'),
    re_path(r'^add-new-site/$', views.add_new_site, name='add_new_site'),
    re_path(r'^rm-site/$', views.rm_site, name='rm_site'),
    re_path(r'^build-pr/$', views.go_build_pr, name='go_build_pr'),
    re_path(r'^add-new-pr/$', views.add_pr_to_basket, name='add_pr_to_basket'),
    re_path(r'^del-pr/$', views.del_pr_in_site, name='del_pr_in_site'),
    re_path(r'^edit-svc/$', views.go_svc_config, name='go_svc_config'),
    re_path(r'^save-svc/$', views.save_svc_config, name='save_svc_config'),
    re_path(r'^valid-ord/$', views.do_ord_valid, name='do_ord_valid'),
]
