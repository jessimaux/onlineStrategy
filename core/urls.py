from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('moderate/courses', views.ModerateCoursesListView.as_view(), name='moderate-courses'),
    path('moderate/profiles', views.ModerateProfilesListView.as_view(), name='moderate-profiles'),
    path('moderate/profiles/<int:pk>', views.ModerateAccountView.as_view(), name='moderate-profile-card'),
    path('route/profile', views.RouteProfileView.as_view(), name='route-profile'),
    path('route/diagnostics', views.DiagnosticListView.as_view(), name='route-diagnostics'),
    path('route/diagnostics/<int:pk>', views.DiagnosticDetailView.as_view(), name='route-diagnostics-item'),
    path('route/diagnostics/result/<int:pk>', views.DiagnosticResultView.as_view(), name='route-diagnostics-result'),
]