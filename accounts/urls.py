from django.urls import path
from . import views

urlpatterns = [
    path('auth', views.AuthView.as_view(redirect_authenticated_user=True), name='auth'),
    path('reg', views.RegView.as_view(), name='reg'),
    path('account/<int:pk>', views.AccountUpdateView.as_view(), name='profile'),
    path('password-change/', views.AccountPasswordChangeView.as_view(), name='password_change'),
    path('password-reset', views.AccountPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/<uidb64>/<token>/',
         views.AccountPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('activate/<uidb64>/<token>/',
         views.AccountActivateView.as_view(),
         name='activate_account'),
]