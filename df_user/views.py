# coding=utf-8
import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from models import *
from hashlib import sha1
from user_decorators import user_login
from df_goods.models import GoodsInfo
# Create your views here.
def register(request):
    context={'title':'注册','top':'0'}
    return render(request, 'df_user/register.html',context)


def login(request):

    context = {'title': '登录','top':'0'}
    return render(request, 'df_user/login.html',context)


def register_handle(request):
    dict=request.POST
    print(dict)
    uname=dict.get('user_name')
    upwd=dict.get('pwd')
    upwd2=dict.get('cpwd')
    uemail=dict.get('email')

    if upwd != upwd2:
        return redirect('/user/register/')


    s1=sha1()
    s1.update(upwd)
    upwd_sha1=s1.hexdigest()

    user=UserInfo()
    user.uname=uname
    user.upwd=upwd_sha1
    user.uemail=uemail
    result = UserInfo.objects.filter(uname=uname).count()

    if result == 0:
        user.save()
    else:
        return redirect('/user/register/')
    return redirect('/user/login/')


def register_valid(request):
    uname=request.GET.get('uname')
    result=UserInfo.objects.filter(uname=uname).count()
    context={'valid':result}
    return JsonResponse(context)


def login_handle(request):
    dict=request.POST
    uname=dict.get('username')
    upwd=dict.get('pwd')
    uname_jz=dict.get('name_jz','0')

    s1=sha1()
    s1.update(upwd)
    upwd_sha1=s1.hexdigest()

    context={'title': '登录','uname':uname,'upwd':upwd,'top':'0'}

    users=UserInfo.objects.filter(uname=uname)
    if len(users)==0:
        # 用户名错误
        context['name_error']='1'
        return render(request, 'df_user/login.html',context)
    else:
        if users[0].upwd == upwd_sha1:#登陆成功
            #记录当前登录的用户
            request.session['uid'] = users[0].id
            request.session['uname'] = uname

            #　重定向　从哪来　回哪去
            path = request.session.get('url_path', '/')
            response = redirect(path)

            if uname_jz == '1':
                response.set_cookie('uname',uname, expires=datetime.datetime.now()+datetime.timedelta(days=7))
            else:
                response.set_cookie('uname','',max_age=-1)

            return response
        else:
            #密码错误
            context['pwd_error']='1'
            return render(request,'df_user/login.html',context)


# @user_login
# def info(request):
#     if request.session.has_key('uid'):
#         return render(request, 'df_user/info.html')
#     else:
#         return redirect('/user/login/')

@user_login
def info(request):
    user=UserInfo.objects.get(pk=request.session['uid'])
    #读取最近浏览商品
    goods_ids = request.COOKIES.get('goods_ids','').split(',')

    goods_list= []
    for gid in goods_ids:
        if gid:
            goods_list.append(GoodsInfo.objects.get(id=gid))


    context={'title':'用户中心','user':user,'goods_list':goods_list}
    return render(request, 'df_user/info.html',context)


@user_login
def order(request):
    return render(request, 'df_user/order.html')


@user_login
def site(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    if request.method == 'POST':
        dict=request.POST
        user.ushou=dict.get('ushou')
        user.uaddress = dict.get('uaddress')
        user.uphone = dict.get('uphone')
        user.save()
    context = {'title': '收货地址', 'user': user}
    return render(request, 'df_user/site.html',context)


def logout(request):
    request.session.flush()
    return redirect('/user/login/')

def islogin(request):
    result=0
    if request.session.has_key('uid'):
        result=1
    return JsonResponse({'islogin':result})