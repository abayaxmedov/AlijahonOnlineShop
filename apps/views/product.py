from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from apps.models import Category, Product, WishList





class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/menu/product-list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        category = Category.objects.filter(slug=slug).first()
        data = super().get_context_data(**kwargs)
        products = Product.objects.all()
        if slug != 'all':
            products = Product.objects.filter(category=category)
        query = self.request.GET.get('query')
        if query:
            products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        data['products'] = products
        data['categories'] = Category.objects.all()
        if self.request.user.is_authenticated:
            data['liked_products_id'] = WishList.objects.filter(user=self.request.user).values_list('product_id',
                                                                                                    flat=True)
        data['session_category'] = category
        return data


class WishListView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, product_id):
        liked = True
        like = WishList.objects.filter(product_id=product_id, user=self.request.user)
        if like.exists():
            like.delete()
            liked = False
        else:
            WishList.objects.create(product_id=product_id, user=self.request.user)
        return JsonResponse({'liked': liked})


class LikeListView(LoginRequiredMixin, ListView):
    queryset = WishList.objects.all()
    template_name = 'apps/menu/wish-list.html'
    context_object_name = 'products'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.filter(product_wishlists__user=self.request.user)
        if self.request.user.is_authenticated:
            data['liked_products_id'] = WishList.objects.filter(user_id=self.request.user).values_list('product_id',
                                                                                                       flat=True)
        return data
