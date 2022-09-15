from django.urls import path
from . import views

urlpatterns = [
    path('moderate/courses', views.ModerateCoursesListView.as_view(), name='moderate-courses'),
    path('moderate/courses/<int:pk>/signs', views.ModerateAccount2CourseListView.as_view(), name='moderate-courses-signs'),
    path('moderate/manuals', views.ModerateManualsListView.as_view(), name='moderate-manuals'),
    path('moderate/methodist', views.ModerateMethodistFormView.as_view(), name='moderate-methodist'),
    path('moderate/diagnostics', views.ModerateDiagnosticsListView.as_view(), name='moderate-diagnostics'),
    path('moderate/profiles', views.ModerateAccountsListView.as_view(), name='moderate-accounts'),
    path('moderate/profiles/<int:pk>', views.ModerateAccountView.as_view(), name='moderate-account'),
]