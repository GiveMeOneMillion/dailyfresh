from django.conf.urls import url
import views

urlpatterns=[
    url('^$', views.index),
    url('^list(\d+)_(\d+)_(\d+)/$',views.list_goods),
    url('^(\d+)/$',views.detail),
]