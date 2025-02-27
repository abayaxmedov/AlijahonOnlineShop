from django.urls import path

from apps.views import AuthTemplateView

urlpatterns = [
    path('auth', AuthTemplateView.as_view(), name='auth'),
]