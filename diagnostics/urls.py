from django.urls import path
from . import views

urlpatterns = [
    path('route/diagnostics', views.DiagnosticListView.as_view(), name='route-diagnostics'),
    path('route/diagnostics/<int:pk>', views.DiagnosticDetailView.as_view(), name='route-diagnostics-item'),
    path('route/diagnostics/result/<int:pk>', views.DiagnosticResultView.as_view(), name='route-diagnostics-result'),
    path('diagnostics/create', views.DiagnosticsCreateView.as_view(), name='diagnostics-create'),
    path('diagnostics/<int:pk>/update', views.DiagnosticsUpdateView.as_view(), name='diagnostics-update'),
    path('diagnostics/<int:pk>/delete', views.DiagnosticsDeleteView.as_view(), name='diagnostics-delete'),
]