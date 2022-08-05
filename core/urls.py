from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('moderate/courses', views.ModerateCoursesListView.as_view(), name='moderate-courses'),
    path('moderate/profiles', views.ModerateProfilesListView.as_view(), name='moderate-profiles'),
    path('moderate/profiles/<int:pk>', views.ModerateAccountView.as_view(), name='moderate-profile-card'),
    path('moderate/manuals', views.ModerateManualsListView.as_view(), name='moderate-manuals'),
    path('moderate/manuals/create', views.ModerateManualsCreateView.as_view(), name='moderate-manuals-create'),
    path('moderate/manuals/<int:pk>/delete', views.ModerateManualsDeleteView.as_view(), name='moderate-manuals-delete'),
    path('moderate/manuals/<int:pk>/update', views.ModerateManualsUpdateView.as_view(), name='moderate-manuals-update'),
    path('route', views.RouteView.as_view(), name='route'),
    path('route/manuals/<int:pk>/add', views.add2route_manual, name='route-add'),
    path('route/manuals/<int:pk>/delete', views.RouteDeleteView.as_view(), name='route-delete'),
    path('route/manuals/<int:pk>/update', views.RouteUpdateView.as_view(), name='route-update'),
    path('route/diagnostics', views.DiagnosticListView.as_view(), name='route-diagnostics'),
    path('route/diagnostics/<int:pk>', views.DiagnosticDetailView.as_view(), name='route-diagnostics-item'),
    path('route/diagnostics/result/<int:pk>', views.DiagnosticResultView.as_view(), name='route-diagnostics-result'),
    path('route/signs/create', views.RouteSignsCreateView.as_view(), name='route-signs-create'),
    path('route/signs/<int:pk>', views.RouteSignsUpdateView.as_view(), name='route-signs-update'),
    path('method/profiles', views.MethodProfilesListView.as_view(), name='method-profiles'),
    path('method/signs', views.MethodSignsListView.as_view(), name='method-signs'),
    path('method/signs/<int:pk>', views.MethodSignsUpdateView.as_view(), name='method-signs-item'),
    path('method/manuals', views.RouteManualsListView.as_view(), name='route-manuals'),
    path('method/profiles/<int:pk>', views.MethodProfilesDetailView.as_view(), name='method-profiles-item'),
    path('method/statistics', views.MethodStatisticsView.as_view(), name='method-statistics'),
    path('moderate/methodist', views.ModerateMethodistFormView.as_view(), name='moderate-methodist')
]