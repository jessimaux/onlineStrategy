from django.urls import path
from . import views

urlpatterns = [
    path('sign/<int:pk>', views.AccountCourseUpdateView.as_view(), name='sign'),
    path('course/<int:pk>/signup', views.CreateAccountCourseView.as_view(), name='course-signup'),
    path('course/create', views.CourseCreateView.as_view(), name='course-create'),
    path('course/<int:pk>/update', views.CourseUpdateView.as_view(), name='course-update'),
    path('course/<int:pk>/delete', views.CourseDeleteView.as_view(), name='course-delete'),
    path('course/<int:pk>/signs', views.AccountCourseListView.as_view(), name='course-view'),
    path('courses', views.CoursesListView.as_view(), name='courses'),
    path('course/<int:pk>', views.CourseView.as_view(), name='course'),
]