import xadmin
from xadmin.layout import Fieldset, Main, Side, Row
from import_export import resources
from apps.courses.models import Course, CouresResource, Video, Lesson,CourseTag,BannerCourse



class MyResource(resources.ModelResource):
    class Meta:
        model = Course


# 通过Inline配置多张表的一次性编辑,注册到CourseAdmin中
class LessonInline(object):
    model = Lesson
    # style = "tab" # 自定义样式之后不能用
    extra = 0
    exclude = ["add_time"]

class CourseResourceInline(object):
    model = CouresResource
    # style = "tab"
    extra = 0
    exclude = ["add_time"]

class CourseAdmin(object):
    import_export_args = {'import_resource_class': MyResource, 'export_resource_class': MyResource}
    list_display = ["name", "teacher","show_image","goto", "learn_times", "degree", "category"]
    search_fields = ["name","teacher","learn_times","degree","category"]
    list_filter = ["name", "teacher__name", "learn_times", "degree", "category"]
    list_editable = ['desc',"learn_times","degree","category"]
    readonly_fields = []# 只读不能更改
    exclude = [] # 隐藏不显示,与上面不能重复
    ordering=["-click_num"] # 默认列表排序
    model_icon = 'fa fa-calculator' #fa要有 fa-也要有 后面是图标名称 http://www.fontawesome.com.cn/faicons/
    inlines = [LessonInline,CourseResourceInline]
    style_fields={
        "detail":"ueditor" # detail表示富文本字段
    }
    # 显示被转义html  {% autoescape off %} {{ course.detail }}{% endautoescape %}

    # 权限绑定,不同的用户返回不同的数据
    # 教师绑定用户一对一关系,使得 其只能查看属于自己的课程.
    # 可以定义返回哪些数据
    def queryset(self):
        qs = super().queryset() # 得到默认返回的数据(所有数据)
        if not self.request.user.is_superuser: # 判断非超级用户数据
            qs = qs.filter(teacher = self.request.user.teacher) # 对数据进行筛选,对课程的teacher字段筛选
            # 由于教师和user是1对1关系,所以能能直接反向从user取teacher
        return qs


    def get_form_layout(self):
        self.form_layout =(
            Main(
                Fieldset("讲师信息",
                         "teacher","course_org",
                          # css_class='unsort no_title'
                ),
                Fieldset("基本信息",
                         "name","desc",
                         Row("learn_times","degree"),
                         Row("category","tag"),

                ),
            ),
            Side(
                Fieldset("访问信息",
                    Row("students","fav_num","click_num")
                ),
                Fieldset("课程信息",
                    "youneed_know","teacher_tell","is_classics"
                )
            ),
            Side(
                Fieldset("封面信息",
                        "image", "notice", "is_banner","is_index"
                         )
            )
        )
        return super(CourseAdmin, self).get_form_layout()




class CouresResourceAdmin:
    list_display = ["name", "course", "file", "add_time"]
    search_fields =  ["name", "course", "file"]
    list_filter =  ["name", "course", "file"]
    list_editable =  ["name", "course", "file"]

class VideoAdmin:
    list_display = ["name", "lessen", "learn_times","url", "add_time"]
    search_fields = ["name", "lessen", "learn_times","url"]
    list_filter = ["name", "lessen", "learn_times","url"]
    list_editable = ["name", "lessen", "learn_times","url"]


class LessonAdmin:
    list_display = ["name", "course", "learn_times","add_time"]
    search_fields = ["name", "course", "learn_times"]
    list_filter = ["name", "course", "learn_times"]
    list_editable = ["name", "course", "learn_times"]

class CourseTagAdmin:
    list_display = ["course", "tag", "add_time"]
    search_fields = [ "course", "tag"]
    list_filter = [ "course", "tag"]
    list_editable = [ "course", "tag"]

class BannerCourseAdmin(object):
    list_display = ["name", "teacher", "learn_times", "degree", "category"]
    search_fields = ["name", "teacher", "learn_times", "degree", "category"]
    list_filter = ["name", "teacher__name", "learn_times", "degree", "category"]
    list_editable = ['desc', "learn_times", "degree", "category"]

    def queryset(self):
        qs = super().queryset()  # 得到默认返回的数据(所有数据)
        qs = qs.filter(is_banner=True)  # 对数据进行筛选,
        return qs





xadmin.site.register(CourseTag,CourseTagAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CouresResource, CouresResourceAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
