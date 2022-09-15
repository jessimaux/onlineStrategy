from django.urls import path
from . import views

urlpatterns = [
    path('method', views.MethodView.as_view(), name='method'),
    path('method/profiles', views.MethodProfilesListView.as_view(), name='method-profiles'),
    path('method/lesson_signs/<int:pk>/update', views.MethodLessonSignsUpdateView.as_view(), name='method-lesson-signs-update'),
    path('method/profiles/<int:pk>', views.MethodProfilesDetailView.as_view(), name='method-profiles-item'),
    path('method/reflections/<int:pk>/update', views.MethodReflectionUpdateView.as_view(), name='method-reflections-update'),
]