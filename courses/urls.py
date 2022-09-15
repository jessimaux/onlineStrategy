from django.urls import path
from . import views

urlpatterns = [
    path('courses', views.CoursesListView.as_view(), name='courses'),
    path('course/<int:pk>', views.CourseView.as_view(), name='course'),
    path('course/create', views.CourseCreateView.as_view(), name='course-create'),
    path('course/<int:pk>/update', views.CourseUpdateView.as_view(), name='course-update'),
    path('course/<int:pk>/delete', views.CourseDeleteView.as_view(), name='course-delete'),

    path('course/sign/<int:pk>/update', views.Account2CourseUpdateView.as_view(), name='course-sign-update'),
    path('course/<int:pk>/signup', views.CreateAccount2CourseView.as_view(), name='course-signup'),
]