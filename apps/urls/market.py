from django.urls import path

from apps.views import MarketListView, ThreadFormView, ThreadListView, ThreedProductDetailView

urlpatterns = [
    path('market/list/<str:slug>', MarketListView.as_view(), name='market-list'),
    path('thread/form', ThreadFormView.as_view(), name='thread-form'),
    path('thread/list', ThreadListView.as_view(), name='thread-list'),
    path("thread/<int:pk>", ThreedProductDetailView.as_view(), name="threed-product"),
]