from django.conf.urls import url
import views
urlpatterns=[
    url(r'order_list/$',views.order_list),
    url(r'handle/$',views.handle),
]