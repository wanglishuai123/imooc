from django.urls import path
from .views import LoginView, LogoutView, RegisterView, DynamicLoginView,UserInfoView,UserMsgView,UserMyCourseView,UploadImageView,ChangePwdView,ChangeMobileView
from .views import MyFavOrg,MyFavCourses,MyFavTeacher
from django.views.decorators.csrf import csrf_exempt

import xadmin

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("d_login/", DynamicLoginView.as_view(), name="d_login"),  # 动态登陆Login
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("info/",UserInfoView.as_view(),name = "info"),
    path("msg/",UserMsgView.as_view(),name = "msg"),
    path("mycourses/",UserMyCourseView.as_view(),name = "mycourses"),
    path("myfavorg/",MyFavOrg.as_view(),name = "myfavorg"),
    path("myfavcourses/",MyFavCourses.as_view(),name = "myfavcourses"),
    path("myfavteacher/",MyFavTeacher.as_view(),name = "myfavteacher"),
    # 头像上传
    path("image/upload/",UploadImageView.as_view(),name = "image"),
    path("update/pwd/",ChangePwdView.as_view(),name = "update_pwd"),# 修改密码
    path("update/mobile/",ChangeMobileView.as_view(),name = "update_mobile"),# 修改手机
]
