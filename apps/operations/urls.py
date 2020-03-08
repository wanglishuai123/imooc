from django.urls import path
from apps.operations.views import AddFavoriteView,AddCommentView



urlpatterns = [
    path("fav_add/", AddFavoriteView.as_view(), name="fav_add"),
    path("add_comment/", AddCommentView.as_view(), name="add_comment"),

    # namespace是用于在下一个其内部的name前面添加namespace,在URL中,使用url:list进行定位

]
