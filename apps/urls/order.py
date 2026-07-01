from django.urls import path

from apps.views import ProductDetailView, OrderFormView, OrderListView

urlpatterns = [
    path("product-order/<str:slug>", ProductDetailView.as_view(), name="product-detail"),
    path('order/form', OrderFormView.as_view(), name='order'),
    path('order/list', OrderListView.as_view(), name='order-list'),
]
