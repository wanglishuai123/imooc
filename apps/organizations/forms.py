from django import forms
from apps.operations.models import UserAsk
import re


"""
class AddAskForm(forms.Form):
    name = forms.CharField(required=True,max_length=20,min_length=2)
    mobile = forms.CharField(required=True,max_length=11,min_length=11)
    course_name = forms.CharField(required=True,max_length=20,min_length=12)



和Operations中model的UserAsk()这个model参数一样
使用ModelForm通过model自动生成Form(解决特别多的字段的问题)
其拥有Model的属性也拥有Form的属性


"""
class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(required=True, max_length=11, min_length=11,error_messages={"required":"手机号不能为空","max_length":"手机号不能多于11位","min_length":"手机号不能少于11位"})


    class Meta:
        model = UserAsk
        fields = ["name","mobile","course_name"]

     # 对Mobile进行合法验证
    def clean_mobile(self):
        # 获取前端手机号
        mobile = self.data.get("mobile")
        # 手机号正则表达式
        regex_mobile = "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$"
        # 预编译
        reg = re.compile(regex_mobile,re.IGNORECASE)

        if reg.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号非法",code="mobile_invalid")
