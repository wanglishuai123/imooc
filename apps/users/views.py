import redis

from django.shortcuts import render, redirect
from django.urls import reverse  # 包含一个Viewname
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, RegisterPostForm
from apps.users.forms import ChangPwdForm, UploadImageForm, UserInfoForm, UpdataMobileForm
from apps.utils.Yunpian import send_single_sms
from apps.utils.random_str import generate_random
from apps.users.models import UserProfile
from edu.settings import REDIS_HOST, REDIS_PORT
from apps.operations.models import UserCourse,UserFavorite,UserMessage,Banner
from apps.organizations.models import CourseOrg,Teacher
from apps.courses.models import Course

from pure_pagination import Paginator, PageNotAnInteger

"""
编写View的步骤:
    1.View代码
    2.配置URL
    3.配置相关的HTML页面  
"""
# 自定义验证方法(配置到Setting)

class CustomAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None



# 全局消息变量
def message_nums(request):
    if request.user.is_authenticated:
        return {"unread_nums":request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}

class ChangeMobileView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def post(self, request, *args, **kwargs):
        mobile_form = UpdataMobileForm(request.POST)
        if mobile_form.is_valid():
            mobile = mobile_form.cleaned_data["mobile"]
            # 已经存在的不能重复注册
            user= request.user

            if user.mobile == mobile:
                return JsonResponse({
                    "mobile": "和当前号码一致!"
                })
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                return JsonResponse({
                    "mobile": "该手机号已经被占用!"
                })
            user = request.user
            user.mobile = mobile
            user.username = mobile
            user.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(mobile_form.errors)

class ChangePwdView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def post(self, request, *args, **kwargs):
        change_pwd_form = ChangPwdForm(request.POST)
        if change_pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")

            user = request.user
            user.set_password(pwd1)
            user.save()
            login(request, request.user)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(change_pwd_form.errors)

class UploadImageView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def post(self, request, *args, **kwargs):
        # 读取图片,并将图片保存(不使用ModelForm如何处理用户上传的头像)
        image_form = UploadImageForm(request.POST, request.FILES,
                                     instance=request.user)  # instance=request.user 表示修改的是哪一个用户 request.FILES修改的哪个字段
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })

        # def save_file(self,file):
        #     with open("C:/Users/nice/Documents/edu/media/head_image/abc.png","wb",) as f:
        #         for chunk in file.chunks():
        #             f.write(chunk)

        # 前端:enctype = "multipartform-data" 和input

        # files = request.FILES["image"]
        # self.save_file(files)
        # pass
        # 1.如果同一个文件上传多次,相同的文件应该如何处理(文件名后添加字符串)
        # 2.文件的并保存路径应该写入到user
        # 3.还没有做表单验证

class UserMsgView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        current_page = "msg"
        my_messages = UserMessage.objects.filter(user=request.user)
        for message in my_messages:
            message.has_read =True
            message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(my_messages, per_page=5, request=request)
        my_messages = p.page(page)

        return render(request, "usercenter-message.html", {
            "current_page": current_page,
            "messages":my_messages,
        })

class UserMyCourseView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        current_page = "mycourse"

        # 获取该用户所有学习的课程对象
        my_user_courses = UserCourse.objects.filter(user=request.user)
        # 从课程对象中提取课程
        courses = [user_course.course for user_course in my_user_courses]

        return render(request, "usercenter-mycourse.html", {
            "current_page": current_page,
            "my_course":courses,
        })

class MyFavOrg(LoginRequiredMixin, View):
    login_url = "/user/login/"
    def get(self, request, *args, **kwargs):
        current_page = "myfav"
        current_page_1 = "org"
        # 获取所有类型是机构的UserFave对象
        my_fav_org = UserFavorite.objects.filter(fav_type=2,user=request.user)
        # 获取他们的ID
        org_id = [user_fav.fav_id for user_fav in my_fav_org]
        # 通过ID获取到他们的数据
        org_list = CourseOrg.objects.filter(id__in=org_id)

        return render(request,"usercenter-fav-org.html",{
            "current_page":current_page,
            "current_page_1": current_page_1,
            'org_list':org_list

        })

class MyFavCourses(LoginRequiredMixin, View):
    login_url = "/user/login/"
    def get(self, request, *args, **kwargs):
        current_page = "myfav"
        current_page_1 = "courses"

        my_fav_courses = UserFavorite.objects.filter(fav_type=1,user=request.user)
        # 获取ID
        courses_id =[user_fav.fav_id for user_fav in my_fav_courses]
        # 通过ID列表获取list
        course_list = Course.objects.filter(id__in=courses_id)

        return render(request, "usercenter-fav-course.html",{
            "current_page":current_page,
            "current_page_1":current_page_1,
            "course_list":course_list

        })

class MyFavTeacher(LoginRequiredMixin, View):
    login_url = "/user/login/"
    def get(self, request, *args, **kwargs):
        current_page = "myfav"
        current_page_1 = "teacher"
        my_fav_teacher = UserFavorite.objects.filter(fav_type=3,user=request.user)
        #获取IDlist
        teacher_id = [fav.fav_id for fav in my_fav_teacher]
        # 通过IDlist获取teacher_list
        teacher_list = Teacher.objects.filter(id__in=teacher_id)

        return render(request, "usercenter-fav-teacher.html",{
            "current_page":current_page,
            "current_page_1": current_page_1,
            "teacher_list":teacher_list
        })

class UserInfoView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        current_page = "info"
        captcha_form = RegisterGetForm()
        return render(request, "usercenter-info.html", {
            "current_page": current_page,
            "captcha_form": captcha_form,
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status": "success",

            })
        else:
            return JsonResponse(user_info_form.errors)

# 手机登陆
class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('index'))  # 重定向到index页面,使用reverse函数反向解析url

        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()

        return render(request, "login.html", {
            "login_form": login_form,
            "next": next,
        })

    def post(self, request, *args, **kwargs):
        dynamic_login = True  # 用于标识是否为动态登陆
        login_form = DynamicLoginPostForm(request.POST)
        if login_form.is_valid():
            # 没有账号依然可以登录
            mobile = login_form.cleaned_data["mobile"]
            # 获取code进行redis认证,判断验证码是否一致.采用利用form进行验证redis,使得代码分离性更好-> form.py
            # 验证用户是否存在
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
                login(request, user)
            else:
                # 新建一个用户
                user = UserProfile(username=mobile)
                password = generate_random(12)  # 生成密码
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)
            next = request.GET.get("next")
            if next:
                return redirect(next, request)  # 需要通过reverse跳转到index
            return redirect(reverse('index'), request)
        else:
            # 为了使得验证码得以显示,所以需要获取有验证码的form传递进来,验证码的form在普通的验证码字段
            d_form = DynamicLoginForm()
            return render(request, "login.html",
                          {"login_form": login_form, "dynamic_login": dynamic_login, "d_form": d_form, })

# 用于发送短信
class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        # 发送验证码的form
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            code = generate_random(6)  # 生成验证码
            re_json = send_single_sms(code, mobile)  # 发送验证码
            if re_json["code"] == 0:  # 如果发送成功
                re_dict["status"] = "success"
                # 连接redis
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
                r.set(str(mobile), code)
                r.expire(str(mobile), 60 * 5)  # 设置验证码5分钟过期
            else:
                re_dict["msg"] = re_json["msg"]  # 返回错误代码给re_dict

        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]
        return JsonResponse(re_dict)  # 返回JsonResponse给Ajax

# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.filter(status=True).order_by("-index") # Banner
        courses = Course.objects.filter(is_index=True)[:6] # 首页课程
        banner_courses = Course.objects.filter(is_banner=True) # banner课程
        course_orgs = CourseOrg.objects.filter(is_index=True)[:15] # 首页机构

        return render(request, "index.html",{
            "banners":banners,
            "courses":courses,
            "banner_courses":banner_courses,
            "course_orgs":course_orgs,
        })

# 账号密码登陆
class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('index'), request)  # 重定向到index页面,使用reverse函数反向解析url

        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()

        return render(request, "login.html", {
            "login_form": login_form,
            "next": next,
        })

    def post(self, request, *args, **kwargs):
        # user_name = request.POST.get('username',"")
        # password = request.POST.get("password","")

        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)  # 用于通过用户名和密码验证用户是否存在

            if user is not None:  # 查询到用户
                login(request, user)
                next = request.GET.get("next")
                if next:
                    return redirect(next, request)  # 需要通过reverse跳转到index
                return redirect(reverse('index'), request)  # 需要通过reverse跳转到index
            else:
                return render(request, "login.html", {"msg": "用户名或者密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('index'), request)

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()

        return render(request, "register.html", {"register_form": register_get_form})

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)

        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            # 新建一个用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return redirect(reverse('index'), request)
        else:
            r_form = RegisterGetForm()
            return render(request, "register.html", {"r_form": r_form, "register_post_form": register_post_form})
