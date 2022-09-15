from django.urls import path
from . import views

urlpatterns = [
    path('route', views.RouteView.as_view(), name='route'),
    path('route/manuals', views.RouteManualsListView.as_view(), name='route-manuals'),
    path('route/manuals/<int:pk>/add', views.add2route_manual, name='route-add'),
    path('route/manuals/<int:pk>/delete', views.RouteDeleteView.as_view(), name='route-delete'),
    path('route/manuals/<int:pk>/update', views.RouteUpdateView.as_view(), name='route-update'),
    path('route/lesson_signs/create', views.RouteLessonSignsCreateView.as_view(), name='route-lesson-signs-create'),
    path('route/lesson_signs/<int:pk>', views.RouteLessonSignsUpdateView.as_view(), name='route-lesson-signs-update'),
    path('route/<int:pk>/reflection/create', views.RouteReflectionCreateView.as_view(), name='route-reflection-create'),
    path('route/reflection/<int:pk>/update', views.RouteReflectionUpdateView.as_view(), name='route-reflection-update'),
    path('moderate/manuals/create', views.ManualsCreateView.as_view(), name='moderate-manuals-create'),
    path('moderate/manuals/<int:pk>/delete', views.ManualsDeleteView.as_view(), name='moderate-manuals-delete'),
    path('moderate/manuals/<int:pk>/update', views.ManualsUpdateView.as_view(), name='moderate-manuals-update'),
]