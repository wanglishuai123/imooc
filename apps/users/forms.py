from django import forms
from captcha.fields import CaptchaField
from edu.settings import REDIS_HOST, REDIS_PORT
import redis
from apps.users.models import UserProfile


class UpdataMobileForm(forms.Form):
    mobile = forms.CharField(required=True, max_length=11, min_length=11,error_messages={"required": "手机号不能为空", "max_length": "您写多了，最多11位长度","min_length": "您写少了，最少11位长度"})
    code = forms.CharField(required=True, max_length=6, min_length=6)

    """
        对每个字段进行单独验证:
        Form提供了一个特定的方法,clean_field()对字段进行单独验证,
        此时获取字段data,就不能从使用cleaned_data取了
        因为cleaned_data的值是在调用了clean()之后才会放到里面的,
        而clean_code()在clean()前面调用,而原始数据都存放在data中,需要使用data.get()去获取,
    """

    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return code

class ChangPwdForm(forms.Form):
    password1 = forms.CharField(required=True , min_length=6)
    password2 = forms.CharField(required=True , min_length=6)

    def clean(self):
        pwd1 = self.data.get("password1")
        pwd2 = self.data.get("password2")
        if pwd1 != pwd2:
            raise forms.ValidationError("密码不一致")
        return self.cleaned_data



class UserInfoForm(forms.ModelForm):
    class Meta:
        model =UserProfile
        fields = ["nick_name","gender","birthday","address"]



class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=11, min_length=6)
    password = forms.CharField(required=True, max_length=18, min_length=6)


class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, max_length=11, min_length=11,error_messages={"required": "手机号不能为空", "max_length": "您写多了，最多11位长度","min_length": "您写少了，最少11位长度"})
    password = forms.CharField(required=True, max_length=18, min_length=6)
    code = forms.CharField(required=True, max_length=6, min_length=6)

    def clean_mobile(self):
        mobile = self.data.get("mobile")
        user = UserProfile.objects.filter(mobile=mobile)
        if user:
            raise forms.ValidationError("该用户已经存在!")
        return mobile

    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return code


# 用于发送短信的Form
class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, max_length=11, min_length=11,error_messages={"required": "手机号不能为空", "max_length": "您写多了，最多11位长度","min_length": "您写少了，最少11位长度"})
    captcha = CaptchaField()


# 用于最终表单提交验证的form
class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True, max_length=11, min_length=11,error_messages={"required": "手机号不能为空", "max_length": "您写多了，最多11位长度","min_length": "您写少了，最少11位长度"})
    code = forms.CharField(required=True, max_length=6, min_length=6)

    """
        对每个字段进行单独验证:
        Form提供了一个特定的方法,clean_field()对字段进行单独验证,
        此时获取字段data,就不能从使用cleaned_data取了
        因为cleaned_data的值是在调用了clean()之后才会放到里面的,
        而clean_code()在clean()前面调用,而原始数据都存放在data中,需要使用data.get()去获取,
    """

    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return code

    """
    clean是form的一个函数,是对每个逻辑验证之后,再对总的逻辑的一个验证.
    返回一个ValidationError与__all__的关键字关联
    

    def clean(self):
        mobile = self.cleaned_data["mobile"]
        code = self.cleaned_data["code"]
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return self.changed_data
    """
