import xadmin
#修改头文件以及脚步显示
class GlobalSetting:
    site_title = "博创后台管理平台"
    site_footer = "博创工作室"
    # menu_style = "accordion"#这个是设置菜单主题

#设置主题
class BaseSeting:
    enable_themes = True
    use_bootswatch = True
#注册
xadmin.site.register(xadmin.views.CommAdminView,GlobalSetting)
xadmin.site.register(xadmin.views.BaseAdminView,BaseSeting)