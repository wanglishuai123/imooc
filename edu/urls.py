"""edu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from django.views.static import serve  # 用户madia目录跳转serve
import xadmin
from apps.users.views import IndexView, SendSmsView
from edu.settings import MEDIA_ROOT


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('user/', include(('apps.users.urls','user'),namespace="user")),
    path('org/', include(('apps.organizations.urls',"organizations"),namespace="org")),
    path('ope/', include(('apps.operations.urls',"operations"),namespace="ope")),
    path('cou/', include(('apps.courses.urls',"courses"),namespace="cou")),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    #namespace是用于在下一个其内部的name前面添加namespace,在URL中,使用url:list进行定位

    # 配置验证码的URL
    path('captcha/', include('captcha.urls')),

    # 配置短信发送的url
    path('send_sms/', csrf_exempt(SendSmsView.as_view()), name="send_sms"),

    # 配置上传文件的访问url
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
]
