from django.urls import path

from apps.views import LoginFormView, ProfileFormView, LogoutView, get_districts, PasswordUpdateFormView, \
    ProfileUserTemplateView

urlpatterns = [
    path('login', LoginFormView.as_view(), name='login'),
    path('profile', ProfileFormView.as_view(), name='profile'),
    path('profile/user', ProfileUserTemplateView.as_view(), name='profile-user'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('get_districts', get_districts, name='get_districts'),
    path('update/password', PasswordUpdateFormView.as_view(), name='update-password'),
]
