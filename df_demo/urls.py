from django.conf.urls import url
import views


urlpatterns=[
    url('^mce/$', views.mce),
    url('^mce2/$', views.mce2),
]