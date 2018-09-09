# coding=utf-8
from django.shortcuts import redirect


def user_login(fun):
    def fun1(request, *args, **kwargs):
        if request.session.has_key('uid'):
            #　如果登录　则继续执行视图
            return fun(request, *args, **kwargs)
        else:
            # 如果没登录　则跳转到登录页
            return redirect('/user/login/')
    return fun1



# def fun1(fun):
#
#     def fun2():
#         pass
#
#     return fun2