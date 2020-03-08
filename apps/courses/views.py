from django.shortcuts import render

from django.views.generic import View
from apps.courses.models import Course, CourseTag,Video,Lesson
from apps.operations.models import UserFavorite, UserCourse, CourseComments
from pure_pagination import Paginator, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


# Create your views here.


class VideoView(View):
    login_url = "/user/login/"

    def get(self, request, course_id, video_id,*args, **kwargs):
        """
        获取课程章节信息
        """
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()

        video = Video.objects.get(id=int(video_id))

        # 将课程与用户绑定
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        lesson = Lesson.objects.filter(course=course)

        # 获取评论内容
        comments = CourseComments.objects.filter(course=course)

        # 获取学习该课程的用户还学过的课程
        # 获取所有学习该课程的对象
        user_courses = UserCourse.objects.filter(course=course)
        # 从对象中获取学习过该课程的所有同学id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 根据ID获取所有学生学习的所有课程的对象
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_num")
        # 获取所有的对象的课程,存储到一个列表中
        related_courses = set()
        for user_course in all_courses:
            if user_course.course.id != course.id:
                related_courses.add(user_course.course)

        return render(request, "course-play.html", {
            "course": course,
            "related_courses": related_courses,
            "comments": comments,
            "all_lesson":lesson,
            "video":video,
        })


class CourseCommentView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节信息
        """
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()
        lesson = Lesson.objects.filter(course=course)


        # 将课程与用户绑定
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        # 获取评论内容
        comments = CourseComments.objects.filter(course=course)

        # 获取学习该课程的用户还学过的课程
        # 获取所有学习该课程的对象
        user_courses = UserCourse.objects.filter(course=course)
        # 从对象中获取学习过该课程的所有同学id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 根据ID获取所有学生学习的所有课程的对象
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_num")
        # 获取所有的对象的课程,存储到一个列表中
        related_courses = set()
        for user_course in all_courses:
            if user_course.course.id != course.id:
                related_courses.add(user_course.course)

        return render(request, "course-comment.html", {
            "course": course,
            "related_courses": related_courses,
            "comments": comments,
            "all_lesson": lesson
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节信息
        """
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()

        lesson = Lesson.objects.filter(course=course)

        # 将课程与用户绑定
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        # 获取所有学习该课程的对象
        user_courses = UserCourse.objects.filter(course=course)
        # 从对象中获取学习过该课程的所有同学id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 根据ID获取所有学生学习的所有课程的对象
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_num")
        # 获取所有的对象的课程,存储到一个列表中
        related_courses = set()
        for user_course in all_courses:
            if user_course.course.id != course.id:
                related_courses.add(user_course.course)

        return render(request, "course-video.html", {
            "course": course,
            "related_courses": related_courses,
            "all_lesson": lesson

        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()

        # 获取收藏状态
        has_fav_course = False
        has_fav_org = False


        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=2):
                has_fav_org = True
        # 是否金牌
        has_gold = course.course_org.is_gold
        has_auth = course.course_org.is_auth

        """
        # 通过课程表内的tag做课程的推荐
        tag = course.tag
        related_courses = []
        if tag:
            related_courses = Course.objects.filter(tag=tag).exclude(id=course_id)[:3] # 使用exclude排除当前课程
            related_courses = Course.objects.filter(tag=tag).exclude(id__in=[course_id])[:3] # 使用__in对比返回一个列表的内容
        """
        # 编写一个课程多个tag进行课程推荐
        tags = course.coursetag_set.all()
        taglist = [tag.tag for tag in tags]  # 简化语法,便利tags中的课程的tag,并且append到taglist中

        course_tags = CourseTag.objects.filter(tag__in=taglist).exclude(
            course__id=course_id)  # 在最后使用course__id的和_id的区别在于前者更强大,还可以__name
        related_courses = set()  # set不允许重复
        for course_tag in course_tags:
            related_courses.add(course_tag.course)
        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_org": has_fav_org,
            "has_fav_course": has_fav_course,
            "has_gold": has_gold,
            "has_auth": has_auth,
            "related_courses": related_courses,
        })


# 课程列表list
class CourseListView(View):
    def get(self, request, *args, **kwargs):

        # 获取全部课程列表
        all_courses = Course.objects.order_by("-add_time")  # 对获取全部数据,并以添加事件倒序
        hot_courses = Course.objects.order_by("-click_num")[:3]

        keywords = request.GET.get("keywords","")
        s_type = "course"
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(category__icontains=keywords))

        # 课程排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("click_num")

        # 对机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=2, request=request)
        orgs = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": orgs,
            "hot_courses": hot_courses,
            "sort": sort,
            "s_type":s_type,
            "keywords":keywords

        })
