from django.urls import path

from apps.views import LoginFormView, ProfileFormView, LogoutView, HomeListView, get_districts, PasswordUpdateFormView, \
    ProductListView, ProductDetailView, WishListView, ProfileUserTemplateView, LikeListView, OrderFormView

urlpatterns = [

    path('', HomeListView.as_view(), name='home'),

]

urlpatterns += [
    path('product/list/<str:slug>', ProductListView.as_view(), name='product-list'),
    path("product-order/<str:slug>", ProductDetailView.as_view(), name="product-detail"),
    path("wishlist/<int:product_id>", WishListView.as_view(), name="product-detail"),
    path("wishlist", LikeListView.as_view(), name="wish-list"),
]

urlpatterns += [
    path('order/form', OrderFormView.as_view(), name='order')
]


#----------------------------  login  ------------------------------

urlpatterns += [
    path('login', LoginFormView.as_view(), name='login'),
    path('profile', ProfileFormView.as_view(), name='profile'),
    path('profile/user', ProfileUserTemplateView.as_view(), name='profile-user'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('get_districts', get_districts, name='get_districts'),
    path('update/password', PasswordUpdateFormView.as_view(), name='update-password'),
]
