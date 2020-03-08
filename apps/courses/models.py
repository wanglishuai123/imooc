from django.db import models
from apps.organizations.models import Teacher, CourseOrg
from datetime import datetime
from DjangoUeditor.models import UEditorField

# Create your models here.
"""
实体 属性 联系
课程 章节 视频 课程资源
"""


class Course(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name="讲师", on_delete=models.CASCADE)
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name="课程名", max_length=50)
    desc = models.CharField(verbose_name="课程描述", max_length=300)
    learn_times = models.IntegerField(verbose_name="学习时长(分钟数)", default=0)
    degree = models.CharField(choices=(('cj', "初级"), ('zj', "中级"), ('gj', "高级")), verbose_name="难度", max_length=50)
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏人数")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(default="后端开发", max_length=20, verbose_name="课程类别")
    tag = models.CharField(default="", verbose_name="课程标签", max_length=10)
    youneed_know = models.CharField(default="", max_length=300, verbose_name="课程须知")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="老师告诉你")
    is_classics = models.BooleanField(default=False, verbose_name="经典课程")
    detail = UEditorField(verbose_name="课程介绍", width=600,height=300,imagePath="courses/ueditor/image",filePath="courses/ueditor/files",default="")
    image = models.ImageField(upload_to="course/%Y/%m", verbose_name="封面图", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    notice = models.CharField(default="",max_length=300,verbose_name="课程公告")
    is_banner = models.BooleanField(default=False,verbose_name="是否广告位")
    is_index = models.BooleanField(default=False,verbose_name="是否首页推荐")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def lesson_num(self):
        return self.lesson_set.all().count()

    # 自定义图片和链接显示在列表

    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<img src='/media/{}' style='height:100px;width:100px;'>".format(self.image)) # 样式需要统一
    show_image.short_description = "页面图"

    def goto(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href = '/cou/{}'>课程页</a>".format(self.id))
    goto.short_description = "页面图"




class CourseTag(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                                verbose_name="课程名称")  # on_delete 表示对应的外键数据删除时是否级联删除（models.CASCADE代表级联删除，models.SET_NULL表示置为空但切记要设置,null=True,blank=True ）
    tag = models.CharField(max_length=20, verbose_name="标签")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = "课程标签"
        verbose_name_plural = verbose_name


class Lesson(models.Model):
    course = models.ForeignKey(Course,
                                on_delete=models.CASCADE,verbose_name="课程名称")  # on_delete 表示对应的外键数据删除时是否级联删除（models.CASCADE代表级联删除，models.SET_NULL表示置为空但切记要设置,null=True,blank=True ）
    name = models.CharField(verbose_name="章节名", max_length=50)
    learn_times = models.IntegerField(verbose_name="学习时长(分钟数)", default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "章节信息"
        verbose_name_plural = verbose_name


class Video(models.Model):
    lessen = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE)  # on_delete 表示对应的外键数据删除时是否级联删除（models.CASCADE代表级联删除，models.SET_NULL表示置为空但切记姚设置,null=True,blank=True ）
    name = models.CharField(verbose_name="视频名称", max_length=100)
    learn_times = models.IntegerField(verbose_name="学习时长(分钟数)")
    url = models.CharField(max_length=1000, verbose_name="访问链接")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name


class CouresResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(verbose_name="资源名称", max_length=100)
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="下载地址", max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

# 使用不同的管理器对同一张表进行管理
class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True  # 设置代理为True,不会生成新的表