import xadmin

from apps.operations.models import UserCourse,UserMessage,UserFavorite,CourseComments,UserAsk,Banner

class UserAskAdmin:
    list_display = ["name", "mobile", "course_name", "add_time"]
    search_fields = ["name", "mobile", "course_name"]
    list_filter = ["name", "mobile", "course_name"]
    list_editable = ["name", "mobile", "course_name"]
class UserCourseAdmin:
    list_display = ["user", "course", "add_time"]
    search_fields = ["user", "course"]
    list_filter = ["user", "course"]
    list_editable = ["user", "course"]

    # 为了避免在修改数据时,继续保存,造成学习人数的错误,重载save_models方法,对保存进行拦截
    # 有这个装饰器的@filter_hook,都可以重载,Django的钩子

    def save_models(self): # 默认的方法是创建和修改都保存,现在只是创建保存,修改不保存
        obj = self.new_obj
        if not obj.id:
            obj.save()
            course = obj.course
            course.students +=1
            course.save()


class UserMessageAdmin:
    list_display = ["user", "message", "has_read","add_time"]
    search_fields = ["user", "message", "has_read"]
    list_filter = ["user", "message", "has_read"]
    list_editable = ["user", "message", "has_read"]

class UserFavoriteAdmin:
    list_display = ["user", "fav_id", "fav_type", "add_time"]
    search_fields = ["user", "fav_id", "fav_type"]
    list_filter = ["user", "fav_id", "fav_type"]
    list_editable = ["user", "fav_id", "fav_type"]
class CourseCommentsAdmin:
    list_display = ["user", "course","comments", "add_time"]
    search_fields = ["user", "course","comments"]
    list_filter = ["user", "course","comments"]
    list_editable = ["user", "course","comments"]

class BannerAdmin:
    list_display = ["title","url","index","status","add_time"]
    search_fields = ["title","url","index","status"]
    list_filter = ["title","url","index","status"]
    list_editable = ["title","url","index","status"]

xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(Banner,BannerAdmin)