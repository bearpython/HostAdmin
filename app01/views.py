# Create your views here.
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
import os,json
from app01 import models
from django.views import View


def login(request):
    error_msg = ""
    if request.method == "POST":
        user = request.POST.get("userEntity.userCode",None)
        pwd = request.POST.get("userEntity.password",None)
        error_msg = ""
        #print(user,pwd)
        user_list = models.User.objects.all()
        #print(user_list)
        if user and pwd:
            if user_list:
                for row in user_list:
                    #print(row.name,row.pwd)
                    if user == row.name and pwd == row.pwd:
                        request.session['username'] = user  # 去session设置值
                        # 使用session之前必须要执行-->python manage.py makemigrations     python manage.py migrate
                        request.session['is_login'] = True
                        request.session.set_expiry(60*60) #自己设置超时时间，默认是2周，在这里设置成一个小时
                        if request.POST.get('rmb', None) == "1":
                            # 对单个用户设置超时时间，用户在前台页面勾选
                            request.session.set_expiry(10)  # 10秒超时
                        return redirect("/app01/index/")
                else:
                    error_msg = "用户名或密码错误"
                    return render(request, "login.html", {"error_msg": error_msg})
        else:
            error_msg = "用户名或密码不能为空"
            return render(request,"login.html",{"error_msg":error_msg})
    else:
        return render(request,'login.html')

def auth(func):
    def inner(request,*args,**kwargs):
        if not request.session.get('is_login', None):
            return redirect('/app01/login/')
        return func(request,*args,**kwargs)
    return inner

@auth
def index(request):
    user = request.session['username']  #去session获取值
    #return render(request,'index.html',{'username':user})  #这个user也可以不传给前端，在前端可以用别的方法取到
    return render(request,'index.html')  #这个user也可以不传给前端，在前端可以用别的方法取到

@auth
def logout(request):
    request.session.clear() #用户注销
    #del request.session['username']a
    return redirect('/app01/login/')

@auth
def introduce(request):
    """网站信息页面"""
    return render(request,'introduce.html')

########################################################主机管理页面##########################################
@auth
def host_list(request):
    user = request.session['username']
    host_l = models.Host.objects.all()
    area_l = models.Area.objects.all()
    status_l = []
    for row in host_l:
        status_l.append(row.get_host_status_id_display())
    #print(status_l)
    status_l = list(set(status_l))
    #print(host_l)
    return render(request,'host_list.html',{'host_l':host_l,'area_l':area_l,'status_l':status_l})

@auth
def host_edit(request,nid):
    """编辑主机,get传参nid"""
    if request.method == "GET":
        host_obj = models.Host.objects.filter(nid=nid).first()
        host_l = models.Host.objects.all()
        area_l = models.Area.objects.all()
        business_l = models.Business.objects.all()
        status_l = []
        for row in host_l:
            status_l.append(row.get_host_status_id_display())
        #print(status_l)
        status_l = list(set(status_l))
        return render(request, 'host_edit.html', {'host_obj': host_obj,'host_l':host_l,'status_l':status_l,'area_l':area_l,'business_l':business_l})
    elif request.method == "POST":
        ret = {"status": True, 'error': None, 'data': None}
        try:
            mes_error = ""
            nid = request.POST.get("nid")
            hostname = request.POST.get("hostname")
            hostip = request.POST.get("hostip")
            hostport = request.POST.get("hostport")
            hostarea = request.POST.get("hostarea")
            hoststatus = request.POST.get("hoststatus")
            hostbusiness = request.POST.get("hostbusiness")
            if hoststatus == "启用":
                hoststatus = 1
            if hoststatus == "挂起":
                hoststatus = 2
            if hoststatus == "停用":
                hoststatus = 3
            if nid and hostname and hostip and hostport and hoststatus and hostbusiness and hostarea:
                models.Host.objects.filter(nid=nid).update(hostname=hostname,ip=hostip,port=hostport,b=hostbusiness,host_status_id=hoststatus,a=hostarea)
            else:
                ret["status"] = False
                ret["error"] = "提交数据不能为空"
        except Exception as e:
            ret["status"] = False
            ret["error"] = "提交数据错误"
        return HttpResponse(json.dumps(ret))
        #return redirect("/app01/host_list/")

@auth
def host_add(request):
    """添加主机"""
    if request.method == "GET":
        host_l = models.Host.objects.all()
        last_nid = models.Host.objects.last()
        area_l = models.Area.objects.all()
        business_l = models.Business.objects.all()
        status_l = []
        for row in host_l:
            status_l.append(row.get_host_status_id_display())
        #print(status_l)
        status_l = list(set(status_l))
        return render(request, 'host_add.html', {'host_l':host_l,'status_l':status_l,'area_l':area_l,'business_l':business_l,'last_nid':last_nid})
    elif request.method == "POST":
        ret = {"status": True, 'error': None, 'data': None}
        try:
            mes_error = ""
            last_nid = request.POST.get("last_nid")
            nid = int(int(last_nid) + 1)
            hostname = request.POST.get("hostname")
            hostip = request.POST.get("hostip")
            hostport = request.POST.get("hostport")
            hostarea = request.POST.get("hostarea")
            hostarea = models.Area.objects.get(id=hostarea)
            hoststatus = request.POST.get("hoststatus")
            hostbusiness = request.POST.get("hostbusiness")
            hostbusiness = models.Business.objects.get(id=hostbusiness)
            #上边两个models.Area.objects.get  是获取外键关联这个对象Area object 1 Business object  这样才能创建数据，具体的数值直接写是不可以的
            if hoststatus == "启用":
                hoststatus = 1
            if hoststatus == "挂起":
                hoststatus = 2
            if hoststatus == "停用":
                hoststatus = 3
            if  hostname and hostip and hostport and hoststatus and hostbusiness and hostarea:
                #print(last_nid,nid,hostname, hostip, hostport, hostarea, hoststatus, hostbusiness)
                models.Host.objects.create(nid=nid,hostname=hostname,ip=hostip,port=hostport,b=hostbusiness,host_status_id=hoststatus,a=hostarea)
            else:
                ret["status"] = False
                ret["error"] = "提交数据不能为空"
        except Exception as e:
            ret["status"] = False
            ret["error"] = "提交数据错误"
        return HttpResponse(json.dumps(ret))
        #return redirect("/app01/host_list/")

@auth
def host_del(request,nid):
    """删除主机,get传参nid"""
    models.Host.objects.filter(nid=nid).delete()
    return redirect("/app01/host_list/")

############################################################################信息维护页面####################################
@auth
def info_manage(request):
    user = models.User.objects.all()
    area = models.Area.objects.all()
    business = models.Business.objects.all()
    return render(request,'info_manage.html',{"user":user,"area":area,"business":business})


from django.views import View
#@auth  ，在这个类上不能使用@login_required这个装饰器，而需要使用method_decorator，并传递一个装饰器（或一个装饰器列表）并告诉应该装饰哪个类
from django.utils.decorators import method_decorator
method_decorator(auth,name='dispatch')
class info_user_add(View):
    """用户添加"""
    def dispatch(self, request, *args, **kwargs):
        """这个方式是父类View里的，如果在这里又定义了一个同名的方法，那就先执行当前的，但是我又想继续用原生的dispatch的功能，那就需要调用一下父类的dispatch方法
        这样在这里就类似于装饰器，可以在请求过来之后做一些处理"""
        #print("before")
        result = super(info_user_add,self).dispatch(request, *args, **kwargs)
        #print("after")
        return result

    def get(self,request):
        type_l = ["管理员","测试","开发"]
        return render(request, 'user_add.html', {'type_l':type_l})

    def post(self,request):
        ret = {"status": True, 'error': None, 'data': None}
        try:
            mes_error = ""
            username = request.POST.get("username")
            userpwd1 = request.POST.get("userpwd1")
            userpwd2 = request.POST.get("userpwd2")
            usertype = request.POST.get("usertype")
            # print(userpwd1,userpwd2)
            if userpwd1 == userpwd2:
                if usertype == "开发":
                    usertype = 1
                if usertype == "测试":
                    usertype = 2
                if usertype == "管理员":
                    usertype = 3
                if  username and usertype and userpwd1:
                    #print(last_nid,nid,hostname, hostip, hostport, hostarea, hoststatus, hostbusiness)
                    models.User.objects.create(name=username,pwd=userpwd1,type_id=usertype)
                else:
                    ret["status"] = False
                    ret["error"] = "提交数据不能为空"
            else:
                ret["status"] = False
                ret["error"] = "确认密码不一致，请重新输入"
        except Exception as e:
            ret["status"] = False
            ret["error"] = "提交数据错误"
        return HttpResponse(json.dumps(ret))
        #return redirect("/app01/host_list/")

method_decorator(auth,name='dispatch')
class info_area_add(View):
    """添加机房位置"""
    def dispatch(self, request, *args, **kwargs):
        result = super(info_area_add,self).dispatch(request, *args, **kwargs)
        return result

    def get(self,request):
        return render(request, 'area_add.html')

    def post(self,request):
        ret = {"status": True, 'error': None, 'data': None}
        try:
            mes_error = ""
            area = request.POST.get("areaname")
            if area:
                models.Area.objects.create(location=area)
            else:
                ret["status"] = False
                ret["error"] = "提交数据不能为空"
        except Exception as e:
            ret["status"] = False
            ret["error"] = "提交数据错误"
        return HttpResponse(json.dumps(ret))

method_decorator(auth,name='dispatch')
class info_business_add(View):
    """添加机房位置"""
    def dispatch(self, request, *args, **kwargs):
        result = super(info_business_add,self).dispatch(request, *args, **kwargs)
        return result

    def get(self,request):
        return render(request, 'business_add.html')

    def post(self,request):
        ret = {"status": True, 'error': None, 'data': None}
        try:
            mes_error = ""
            businessname = request.POST.get("businessname")
            businesscode = request.POST.get("businesscode")
            if businessname and businesscode:
                models.Business.objects.create(caption=businessname,code=businesscode)
            else:
                ret["status"] = False
                ret["error"] = "提交数据不能为空"
        except Exception as e:
            ret["status"] = False
            ret["error"] = "提交数据错误"
        return HttpResponse(json.dumps(ret))

method_decorator(auth,name='dispatch')
class info_user_edit(View):
    """添加机房位置"""
    def dispatch(self, request, *args, **kwargs):
        result = super(info_user_edit,self).dispatch(request, *args, **kwargs)
        return result

    def get(self,request,id):
        user = models.User.objects.filter(id=id).first()
        type_l = ["管理员","测试","开发"]
        type = user.get_type_id_display()
        return render(request, 'user_edit.html', {'type':type,'type_l':type_l,"user":user})

    def post(self,request,id):
        ret = {"status": True, 'error': None, 'data': None}
        try:
            mes_error = ""
            username = request.POST.get("username")
            oldpwd = request.POST.get("oldpwd")
            newpwd = request.POST.get("newpwd")
            usertype = request.POST.get("usertype")
            #print(id, username, oldpwd,newpwd, usertype)
            user = models.User.objects.filter(id=id).first()
            if usertype == "开发":
                usertype = 1
            if usertype == "测试":
                usertype = 2
            if usertype == "管理员":
                usertype = 3
            if oldpwd == user.pwd:
                if oldpwd != newpwd:
                    #print(id,username,newpwd,usertype)
                    if id and username and newpwd and usertype:
                        models.User.objects.filter(id=id).update(name=username,pwd=newpwd,type_id=usertype)
                    else:
                        ret["status"] = False
                        ret["error"] = "提交数据不能为空"
                else:
                    ret["status"] = False
                    ret["error"] = "新旧密码不能相同"
            else:
                ret["status"] = False
                ret["error"] = "旧密码输入错误，请重新输入"
        except Exception as e:
            ret["status"] = False
            ret["error"] = "提交数据错误"
        return HttpResponse(json.dumps(ret))


method_decorator(auth,name='dispatch')
class info_area_edit(View):
    """添加机房位置"""
    def dispatch(self, request, *args, **kwargs):
        result = super(info_area_edit,self).dispatch(request, *args, **kwargs)
        return result

    def get(self,request,id):
        location = models.Area.objects.filter(id=id).first()
        return render(request, 'area_edit.html', {'location':location})

    def post(self,request,id):
        ret = {"status": True, 'error': None, 'data': None}
        try:
            mes_error = ""
            location = request.POST.get("location")
            if id and location:
                models.Area.objects.filter(id=id).update(location=location)
            else:
                ret["status"] = False
                ret["error"] = "提交数据不能为空"
        except Exception as e:
            ret["status"] = False
            ret["error"] = "提交数据错误"
        return HttpResponse(json.dumps(ret))

method_decorator(auth,name='dispatch')
class info_business_edit(View):
    """添加机房位置"""
    def dispatch(self, request, *args, **kwargs):
        result = super(info_business_edit,self).dispatch(request, *args, **kwargs)
        return result

    def get(self,request,id):
        business = models.Business.objects.filter(id=id).first()
        return render(request, 'business_edit.html', {'business':business})

    def post(self,request,id):
        ret = {"status": True, 'error': None, 'data': None}
        try:
            mes_error = ""
            business = request.POST.get("business")
            code = request.POST.get("code")
            if id and business and code:
                models.Business.objects.filter(id=id).update(caption=business,code=code)
            else:
                ret["status"] = False
                ret["error"] = "提交数据不能为空"
        except Exception as e:
            ret["status"] = False
            ret["error"] = "提交数据错误"
        return HttpResponse(json.dumps(ret))

@auth
def info_user_del(request,id):
    """删除用户,get传参id"""
    models.User.objects.filter(id=id).delete()
    return redirect("/app01/info_manage/")

@auth
def info_area_del(request,id):
    """删除用户,get传参id"""
    models.Area.objects.filter(id=id).delete()
    return redirect("/app01/info_manage/")

@auth
def info_business_del(request,id):
    """删除用户,get传参id"""
    models.Business.objects.filter(id=id).delete()
    return redirect("/app01/info_manage/")



###########################################################用户数据初始化接口################################
def init(request):
    '''Manage user initialization'''
    dic = {"name":"bfax","pwd":"123","type_id":1}
    models.User.objects.create(**dic)
    return HttpResponse('OK')