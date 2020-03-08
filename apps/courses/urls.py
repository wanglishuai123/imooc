from django.urls import path
from apps.courses.views import CourseListView,CourseDetailView,CourseLessonView,CourseCommentView,VideoView


urlpatterns = [
    path("list/", CourseListView.as_view(), name="list"),
    path("<int:course_id>/", CourseDetailView.as_view(), name="detail"),
    path("<int:course_id>/lesson", CourseLessonView.as_view(), name="lesson"),
    path("<int:course_id>/comment", CourseCommentView.as_view(), name="comment"),
    path("<int:course_id>/video/<int:video_id>/", VideoView.as_view(), name="video"),
]
