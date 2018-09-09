from django.contrib import admin
from models import *

# Register your models here.
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id','gtitle','gprice','gclick','gtype']
    list_per_page = 10

admin.site.register(TypeInfo)
admin.site.register(GoodsInfo,GoodsAdmin)