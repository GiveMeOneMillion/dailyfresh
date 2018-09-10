# coding=utf-8
from django.db import transaction
from django.shortcuts import render, redirect

from datetime import datetime
# Create your views here.
from df_cart.models import CartInfo
from df_user.models import UserInfo
from models import *


def order_list(request):
    uid=request.session.get('uid')
    user=UserInfo.objects.get(pk=uid)

    dict=request.POST
    cids=dict.getlist('cid')
    cart_list=CartInfo.objects.filter(pk__in=cids)
    context={'title':'订单页面','cart_list':cart_list,'user':user}
    return render(request, 'df_order/order_list.html',context)


@transaction.atomic
def handle(request):

    sid=transaction.savepoint()

    try:
        dict=request.POST
        cids=dict.getlist('cid')
        addr=dict.get('addr')
        uid=request.session.get('uid')
        '''
        创建订单主表对象
        判断商品库存是否足够
        便历购物车信息　创建订单祥表对象
        将商品数量减少
        '''
        order=OrderInfo()
        order.oid='%s%d'%(datetime.now().strftime('%Y%m%d%H%M%S'),uid)
        order.user_id=uid
        order.ototal=0
        order.oaddress=addr
        order.save()

        total=0
        cartlist=CartInfo.objects.filter(pk__in=cids)
        for cart in cartlist:
            if cart.count>cart.goods.gkucun:
                # 库存不足　放弃购买　回滚
                transaction.savepoint_rollback(sid)
                return redirect('/cart/')
            else:
                #　库存足够　创建订单祥表
                detail=OrderDetailInfo()
                detail.goods=cart.goods
                detail.price=cart.goods.gprice
                detail.count=cart.count
                detail.order=order
                detail.save()

                #计算商品总价
                total+=detail.price*detail.count
                #修改库存数量
                goods=cart.goods
                goods.gkucun-=cart.count
                goods.save()
                #删除购物车
                cart.delete()


        #保存总价
        order.ototal=total
        order.save()
        #购买成功
        transaction.savepoint_commit(sid)
        return redirect('/user/order/')
    except:
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')
