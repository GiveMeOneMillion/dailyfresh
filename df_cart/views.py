#coding=utf-8
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render

from df_user.user_decorators import user_login
from models import *

# Create your views here.
def add(request):
    dict = request.GET
    gid = int(dict.get('gid'))
    count = int(dict.get('count'))

    uid = request.session.get('uid')


    #查询当前用户是否已经购买商品

    carts = CartInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(carts)==0:

        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = int(gid)
        cart.count = int(count)
        cart.save()
    else:
        cart=carts[0]
        cart.count += count
        cart.save()

    count=calc(uid)
    return JsonResponse({'isok':1,'count':count})

@user_login
def cart(request):
    cart_list=CartInfo.objects.filter(user_id=request.session.get('uid'))
    context={'title':'购物车','cart_list':cart_list}
    return render(request,'df_cart/cart.html',context)

def delcart(request):
    try:
        dict = request.GET
        cid = dict.get('cid')
        cart=CartInfo.objects.get(id=cid)
        cart.delete()
        return JsonResponse({'isok':1})
    except:
        return JsonResponse({'isok':0})


def set(request):
    dict = request.GET
    cid = dict.get('cid')
    count = dict.get('count')
    isok=0
    try:

        cart=CartInfo.objects.get(id=cid)
        cart.count=int(count)
        cart.save()
        isok=1

    except:
        isok=0

        return JsonResponse({'isok':isok})

def count(request):
    count = calc(request.session.get('uid'))
    return JsonResponse({'count':count})

def calc(uid):
    count =CartInfo.objects.filter(user_id=uid).aggregate(Sum('count'))
    print count
    return count.get('count__sum')