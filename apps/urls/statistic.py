from django.urls import path

from apps.views.statistic import StatisticTemplateView

urlpatterns = [
    path('statistic', StatisticTemplateView.as_view(), name='statistic-list')
]