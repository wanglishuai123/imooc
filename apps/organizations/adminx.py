import xadmin

# Register your models here.


from apps.organizations.models import City,CourseOrg,Teacher


class CityAdmin:
    list_display = ["name", "desc", "add_time"]
    search_fields = ["name", "desc", "add_time"]
    list_filter = ["name", "desc", "add_time"]
    list_editable = ["name", "desc", "add_time"]


class CourseOrgAdmin:

    list_display = ["name", "desc", "category", "address","add_time"]
    search_fields = ["name", "desc", "category", "address"]
    list_filter = ["name", "desc", "category", "address"]
    list_editable = ["name", "desc", "category", "address"]


class TeacherAdmin:
    list_display = ["name", "work_years", "courseorg","work_company","add_time"]
    search_fields = ["name", "work_years", "courseorg","work_company"]
    list_filter = ["name", "work_years", "courseorg","work_company"]
    list_editable = ["name", "work_years", "courseorg","work_company"]


xadmin.site.register(City,CityAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)


