from django.urls import path

from apps.views import OperatorTemplateView, OperatorOrderDetailView, OrderUpdateView

urlpatterns = [
    path('operator', OperatorTemplateView.as_view(), name='operator'),
    path('operator/order/detail/<int:pk>', OperatorOrderDetailView.as_view(), name='order-detail'),
    path('operator/order/change/<int:pk>', OrderUpdateView.as_view(), name='order-change'),
]
