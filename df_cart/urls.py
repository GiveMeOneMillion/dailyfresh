from django.conf.urls import url
import views

urlpatterns=[
    url(r'add/$',views.add),
    url('^$',views.cart),
    url(r'^delcart/$',views.delcart),
    url(r'^set/$',views.set),
    url(r'^count/$',views.count)
]