from django.shortcuts import render

from django.views.generic.base import View
from django.http import JsonResponse
from apps.operations.forms import UserFavForm, CourseCommentForm
from apps.operations.models import UserFavorite, CourseComments
from apps.courses.models import Course
from apps.organizations.models import CourseOrg, Teacher


class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        """
        添加评论
        """
        # 判断用户是否登陆
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登陆"
            })

        comment_form = CourseCommentForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data["course"]
            comments = comment_form.cleaned_data["comments"]

            comment = CourseComments()
            comment.user = request.user
            comment.comments = comments
            comment.course = course
            comment.save()
            return JsonResponse({
                "status": "success",
            })

        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


class AddFavoriteView(View):
    def post(self, request, *args, **kwargs):
        """
        取消收藏,收藏

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断用户是否登陆
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登陆"
            })
        # 表单验证
        fav_form = UserFavForm(request.POST)
        if fav_form.is_valid():
            fav_id = fav_form.cleaned_data["fav_id"]
            fav_type = fav_form.cleaned_data["fav_type"]

            # 判断数据是否被收藏
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            # 如果已经被收藏
            if existed_records:
                # 删除数据
                existed_records.delete()
                if fav_type == 1:  # 课程
                    course = Course.objects.get(id=fav_id)
                    course.fav_num -= 1
                    course.save()
                elif fav_type == 2:  # 机构
                    course = CourseOrg.objects.get(id=fav_id)
                    course.fav_num -= 1
                    course.save()
                elif fav_type == 3:  # 教师
                    course = Teacher.objects.get(id=fav_id)
                    course.fav_num -= 1
                    course.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "收藏",
                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏",
                })
        else:

            # 添加数据
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误",
            })
