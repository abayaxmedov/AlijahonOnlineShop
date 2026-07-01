from django.urls import path

from apps.views import HomeListView, CompetitionListView, ThreadRequestTemplateView, DiogramTemplateView

urlpatterns = [

    path('', HomeListView.as_view(), name='home'),
    path('competition', CompetitionListView.as_view(), name='competition'),
    path('thread/request', ThreadRequestTemplateView.as_view(), name='thread-request'),
    path('diogramm', DiogramTemplateView.as_view(), name='diogram'),

]
