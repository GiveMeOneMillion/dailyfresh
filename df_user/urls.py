from django.conf.urls import url
import views

urlpatterns=[
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^register_handle/$', views.register_handle),
    url(r'^register_valid/$', views.register_valid),
    url(r'^login_handle/$', views.login_handle),
    url(r'^info/$', views.info),
    url(r'^order/$', views.order),
    url(r'^site/$', views.site),
    url(r'^logout/$', views.logout),
    url(r'^islogin/$', views.islogin),
]