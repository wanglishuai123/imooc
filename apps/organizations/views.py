from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
import json
from pure_pagination import Paginator, PageNotAnInteger
from apps.organizations.models import CourseOrg, City,Teacher
from apps.organizations.forms import AddAskForm
from apps.operations.models import UserFavorite
from django.db.models import Q
class TeacherDetailView(View):
    def get(self,request,teacher_id,*args,**kwargs):
        # 获取教师信息

        teacher = Teacher.objects.get(id=int(teacher_id))
        courses = teacher.course_set.all()[:3]
        course_org = teacher.courseorg
        org_teacher = course_org.teacher_set.order_by("-click_num")[:3]

        # 获取收藏状态
        has_fav_teacher = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher_id, fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav_org = True

        return render(request,"teacher-detail.html",{
            "teacher":teacher,
            "courses":courses,
            "org_teacher":org_teacher,
            "has_fav_teacher":has_fav_teacher,
            "has_fav_org":has_fav_org,
        })

class TeacherView(View):
    def get(self,request,*args,**kwargs):
        teachers = Teacher.objects.all()

        #根据人气排序
        sort = request.GET.get("sort","")
        if sort=="hot":
            teachers = teachers.order_by("-click_num")
        work_year_teacher = teachers.order_by("-work_years")[:3]

        keywords = request.GET.get("keywords", "")
        s_type = "teacher"
        if keywords:
            teachers = teachers.filter(
                Q(name__icontains=keywords) | Q(points__icontains=keywords) | Q(work_postion__icontains=keywords))
        # 对讲师开始分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, per_page=2, request=request)
        teach = p.page(page)


        return render(request,"teachers-list.html",{
            "teachers":teach,
            "sort":sort,
            "work_year_teacher":work_year_teacher,
            "s_type":s_type,
            "keywords":keywords
        })



class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()
        all_teacher = course_org.teacher_set.all()  # 外键反向去数据
        all_courses = course_org.course_set.all()  # 外键反向去数据

        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id):
                has_fav =True

        return render(request, "org-detail-homepage.html", {
            "current_page": current_page,
            "course_org": course_org,
            "all_techer": all_teacher,
            "all_course": all_courses,
            "has_fav":has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        all_teacher = course_org.teacher_set.all()  # 外键反向取数据,获得teacher
        return render(request, "org-detail-teachers.html", {
            "current_page": current_page,
            "course_org": course_org,
            "all_techer": all_teacher,
            "has_fav": has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "courses"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()

        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        all_courses = course_org.course_set.all()  # 外键反向去数据
        return render(request, "org-detail-course.html", {
            "current_page": current_page,
            "course_org": course_org,
            "all_course": all_courses,
            "has_fav": has_fav,
        })


class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()

        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        all_courses = course_org.course_set.all()  # 外键反向去数据
        return render(request, "org-detail-desc.html", {
            "current_page": current_page,
            "course_org": course_org,
            "all_course": all_courses,
            "has_fav": has_fav,
        })


class AddAskView(View):
    """
    处理用户咨询
    """

    def post(self, request, *args, **kwargs):
        ask_form = AddAskForm(request.POST)
        if ask_form.is_valid():
            ask_form.save(commit=True)
            return JsonResponse({
                "status": "success"
            })
        else:
            errors = ask_form.errors  # 获取错误信息
            error_str = json.dumps(errors)  # 转换为str
            error_dict = json.loads(error_str)  # 转化为dict
            msg = ""  # 设定一个自定义msg字符串,用来返回错误
            for value in error_dict.values():  # 遍历error_dict的values,毕竟错误不止一个
                msg = "".join((str(msg), "\n", str(value)))  # 组装
            return JsonResponse({
                "status": "fail",
                "msg": "添加出错" + "\n" + msg.strip().replace('[', '').replace(']', '').replace('\'', "")
            })


class OrgView(View):

    def get(self, request, *args, **kwargs):
        # 从数据库中获取数据
        all_orgs = CourseOrg.objects.all()  # 获取全部机构数据
        all_citys = City.objects.all()  # 获取全部城市数据

        keywords = request.GET.get("keywords", "")
        s_type = "org"
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(category__icontains=keywords))

        # 对机构进行排名
        hot_orgs = all_orgs.order_by("click_num")[:3]

        # 通过机构类别对课程机构进行筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 通过所在城市对机构进行筛选
        city_id = request.GET.get("city", "")
        if city_id:
            if city_id.isdigit():  # 判断是否为数字
                all_orgs = all_orgs.filter(city_id=city_id)

        org_nums = all_orgs.count()  # 获取个数

        # 对机构进行排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")  # - 代表倒序,无代表正序
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")

        # 对机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, per_page=5, request=request)
        orgs = p.page(page)
        return render(request, "org-list.html",
                      {"all_orgs": orgs,
                       "org_nums": org_nums,
                       "all_citys": all_citys,
                       "category": category,
                       "city_id": city_id,
                       "sort": sort,
                       "hot_orgs": hot_orgs,
                       "s_type":s_type,
                      "keywords":keywords,
                       })

    def post(self, *args, **kwargs):
        pass
