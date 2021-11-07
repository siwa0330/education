from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views import View
from . import models
from education import urls

#django自带的认证，登录，注销（不好用？不会用）
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class register(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        #1.获取客户注册信息
        username = request.POST.get('username')
        realname = request.POST.get('realname')
        usertype = request.POST.get('usertype')
        workid = request.POST.get('workid')
        collegetype = request.POST.get('collegetype')
        password = request.POST.get('password')
        re_pwd = request.POST.get('re_pwd')
        #2.校验用户名是否被占用
        try:
            models.User.objects.get(username=username)
            error_msg = '用户名已被注册'
            return render(request, 'register.html', {'error_msg': error_msg})
        except:
            pass
        #3.校验数据完整性
        if not all([username, realname, usertype, collegetype, password, re_pwd]):
            error_msg = '请完整填写数据'
            return render(request, 'register.html', {'error_msg': error_msg})

        #4.校验数据长度是否合法
        if len(realname) > 30 or len(workid) > 10 or len(password)>30:
            error_msg = '数据格式不正确'
            return render(request, 'register.html', {'error_msg': error_msg})
        #5.校验密码输入是否相同
        if re_pwd != password:
            error_msg = '两次输入密码不相同'
            return render(request, 'register.html', {'error_msg': error_msg})
        #5.在数据库中插入一条用户数据
        models.User.objects.create(username=username,
                                   realname=realname,
                                   usertype=usertype,
                                   collegetype=collegetype,
                                   password=password,
                                   workid=workid
                                   )
        #back_userinfo = models.User.objects.get(username=username)
        return redirect('/login')

class my_login(View):
    def get(self, request):
        if request.session.get('id'):
            return redirect('/index')
        else:
            return render(request, 'login.html')
    def post(self, request):
        #1.校验数据完整性
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print(username,password)
        if not all([username, password]):
            error_msg = '用户名或密码不能为空'
            return render(request, 'login.html', {'error_msg': error_msg})
        #2.校验用户名是否已经注册，若注册，则判断密码是否正确。若未注册，返回错误信息
        try:
            obj = models.User.objects.filter(username=username).get()
            #print(obj.id,obj.password,obj.realname)
            if password == obj.password:
                #密码正确，将用户id写入session
                request.session['id'] = obj.id
                request.session['username'] = obj.username

                #print(obj.usertype)
                return redirect('/index')
            else:
                error_msg = '用户名或密码不正确'
                return render(request, 'login.html', {'error_msg': error_msg})
        except :
            error_msg = '用户名不存在'
            return render(request, 'login.html', {'error_msg': error_msg})


class my_logout(View):

    def get(self, request):
        #删除session信息，跳转回登录页面
        request.session.flush()
        return redirect('/login/')

class info(View):

    def get(self, request):
        if request.session.get('id'):
            id = request.session.get('id')
            obj = models.User.objects.filter(id=id).get()
            return render(request, 'info.html', {'obj': obj})
        else:
            return render(request, 'login.html')


class index(View):

    def get(self, request):
        if request.session.get('id'):
            id = request.session.get('id')
            obj = models.User.objects.filter(id=id).get()
            #查询用户发布（添加）过的所有课程id（返回queryset对象）
            lesson_id = models.user2lesson.objects.filter(uit_id=id).all().values('lid_id')
            #print(lesson_id)   输出：<QuerySet [{'lid_id': 1}, {'lid_id': 2}]>

            #查询用户发布（添加）过的所有课程详细信息（返回object对象：[(obj),(obj),...]）
            lesson_list = []

            for index in range(len(lesson_id)):
                temp_obj = models.lesson.objects.get(id=lesson_id[index]['lid_id'])
                #print(temp_obj)    lesson object (1) lesson object (2)
                #根据查询出来的每一条课程对象，利用里面记录的teacher_id,反查教师姓名
                teacher_obj = models.User.objects.filter(id=temp_obj.teacher_id).get()
                temp_list = [temp_obj.title, temp_obj.desc, teacher_obj.realname, temp_obj.id]

                lesson_list.append(temp_list)
            #print(lesson_list)    [<lesson: lesson object (1)>, <lesson: lesson object (2)>]
            #将lesson_list包装成[(1, obj), (2, obj),...]
            lesson_list = list(enumerate(lesson_list, 1))


            return render(request, 'index.html', {'lesson_list': lesson_list, 'obj': obj})
        else:
            return render(request, 'login.html')

class edit_info(View):
    def get(self, request):
        id = request.session.get('id')
        obj = models.User.objects.filter(id=id).get()
        return render(request, 'edit_info.html', {'obj': obj})
    def post(self, request):
        id = request.session.get('id')
        #username = request.POST.get('username')
        realname = request.POST.get('realname')
        workid = request.POST.get('workid')
        collegetype = request.POST.get('collegetype')
        desc = request.POST.get('desc')
        #print(id,username, realname, desc, workid,collegetype)
        obj = models.User.objects.filter(id=id)
        obj.update(realname=realname, workid=workid,
                   collegetype=collegetype, desc=desc)
        #print(ret.query)

        return redirect('/info/')

class submit_lesson(View):

    def get(self, request):
        if request.session.get('id'):
            id = request.session.get('id')
            obj = models.User.objects.filter(id=id).get()
            return render(request, 'submit_lesson.html', {'obj': obj})
        else:
            return render(request, 'login.html')

    def post(self, request):
        #接收课程信息
        id = request.session.get('id')
        obj = models.User.objects.filter(id=id).get()

        #下面两条信息接收不到
        # realname = request.POST.get('realname')
        # collegetype = request.POST.get('collegetype')

        title = request.POST.get('title')
        desc = request.POST.get('desc')
        #print(id, obj.realname, obj.collegetype, title, desc)
        red = models.lesson.objects.update_or_create(title=title, desc=desc, collegetype=obj.collegetype, teacher_id=id)
        #print(red)
        models.user2lesson.objects.update_or_create(uit_id=id, lid_id=red[0].id)
        return redirect('/index/')

class add_lesson(View):

    def get(self, request):
        if request.session.get('id'):
            #获取个人信息
            id = request.session.get('id')
            obj = models.User.objects.filter(id=id).get()
            #获取个人已经添加过的课程信息
            u2l_objs = models.user2lesson.objects.filter(uit_id=id).all()
            lesson_id_list = []
            for u2l_obj in u2l_objs:
                lesson_id_list.append(u2l_obj.lid_id)

            #获取所有课程
            lesson_list = models.lesson.objects.exclude(id__in=lesson_id_list).all()
            info_list = []
            for lesson_obj in lesson_list:
                teacher_obj = models.User.objects.filter(id=lesson_obj.teacher_id).get()
                temp_list = [lesson_obj.title, lesson_obj.desc, teacher_obj.realname, lesson_obj.collegetype]
                info_list.append(temp_list)
            info_list = list(enumerate(info_list, 1))


            return render(request, 'add_lesson.html', {'obj': obj, 'info_list': info_list})
        else:
            return render(request, 'login.html')


class choice_lesson(View):
    def get(self, request):

        #接收前端的数据
        id = request.session.get('id')
        title = request.GET.get('title')
        desc = request.GET.get('desc')

        #print(id, title, desc)
        #从数据库中查询课程id 并在关系表中添加一条数据
        obj = models.lesson.objects.filter(title=title, desc=desc).get()
        #判断课程是否已经被添加过
        #若已被添加停留在当前页面；未被添加，跳回到个人课程页，并增加一条信息
        #print(obj.id)
        try:
            models.user2lesson.objects.filter(uit_id=id, lid_id=obj.id).get()
            return render(request, 'error_page.html')

        except:
            red = models.user2lesson.objects.update_or_create(uit_id=id, lid_id=obj.id)
            return redirect('/index/')

    def post(self, request):
        ret = {'status': True, 'message': None}
        try:
            id = request.session.get('id')
            collegetype = request.POST.get('collegetype')
            realname = request.POST.get('realname')
            #print(realname)
            desc = request.POST.get('desc')
            title = request.POST.get('title')
            lesson_obj = models.lesson.objects.filter(title=title, desc=desc).get()
            models.user2lesson.objects.update_or_create(lid_id=lesson_obj.id, uit_id=id)
        except Exception as e:
            ret['status'] = False
            ret['message'] = '异常'
        import json
        return HttpResponse(json.dumps(ret))

class del_lesson(View):
    def get(self, request):
        if request.session.get('id'):
            id = request.session.get('id')
            lesson_id = request.GET.get('nid')
            models.user2lesson.objects.filter(uit_id=id, lid_id=lesson_id).delete()
            return redirect('/index')
        else:
            return redirect('/login')



