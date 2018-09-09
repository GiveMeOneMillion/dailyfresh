class UrlMiddleware:
    def process_view(self,request,view_name,view_args,view_kwargs):
        print '---%s'%request.path
        if request.path not in ['/user/register/',
                                '/user/register_handle/',
                                '/user/register_valid/',
                                '/user/login/',
                                '/user/login_handle/',
                                '/user/logout/',
                                '/user/islogin/,'
                                ]:
            request.session['url_path']=request.get_full_path()

'''
https://www.kgc.cn/python/?name=zdb&age=22&scores=750#abc

path--->/python/
get_full_path()--->/python/?name=zdb&age=22&scores=750#abc
'''