from django.urls import path

from apps.views import ProductListView, WishListView, LikeListView


urlpatterns = [
    path('product/list/<str:slug>', ProductListView.as_view(), name='product-list'),
    path("wishlist/<int:product_id>", WishListView.as_view(), name="wishlist"),
    path("wishlist", LikeListView.as_view(), name="wish-list"),
]
