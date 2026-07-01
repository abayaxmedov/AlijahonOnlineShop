from django.urls import path

from apps.views import TestTemplateView

urlpatterns = [
    path('test', TestTemplateView.as_view()),

]