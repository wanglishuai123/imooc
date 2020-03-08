from django.db import models
from datetime import datetime
# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name="城市名称")
    desc = models.TextField(verbose_name="描述")  # 后期改富文本
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name="描述")  # 后期改富文本
    tag = models.CharField(default="全国知名", verbose_name="机构标签", max_length=10)
    category = models.CharField(default="pxjg", verbose_name="机构类别", max_length=4,
                                choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")))
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo", max_length=100,blank=True)
    address = models.CharField(max_length=150, verbose_name="机构地址")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    city = models.ForeignKey(City, verbose_name="所在城市", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    is_auth = models.BooleanField(default=False,verbose_name="是否认证")
    is_gold = models.BooleanField(default=False,verbose_name="是否金牌")
    is_index = models.BooleanField(default=False,verbose_name="是否首页展示")

    def courses(self):
        courses = self.course_set.filter(is_classics=True)[:3]# 反向取外键关联数据(需要本类在第二个model中是外键)|对经典课程数量切片
        return courses

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "教育机构"
        verbose_name_plural = verbose_name

from apps.users.models import UserProfile
class Teacher(models.Model):
    user = models.OneToOneField(UserProfile,null=True,blank=True,verbose_name="用户",on_delete=models.SET_NULL)
    courseorg = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构",default="")
    name = models.CharField(max_length=50, verbose_name="讲师名称")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_postion = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    fav_num = models.IntegerField(default=0, verbose_name="收藏人数")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    age = models.IntegerField(default=18, verbose_name="年龄")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "讲师"
        verbose_name_plural = verbose_name

