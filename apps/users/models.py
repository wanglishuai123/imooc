from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.

CENDER_CHOICES = (
    ("male", "男"),
    ("female", '女')

)


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", choices=CENDER_CHOICES, max_length=6)
    address = models.CharField(max_length=100, verbose_name="地址", default="")
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    image = models.ImageField(upload_to="head_image/%Y/%m", default="default.jpg", max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username
    def unread_nums(self):
        return self.usermessage_set.filter(has_read=False).count()
#
#
# class model.Model(models.Model):
#     add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
