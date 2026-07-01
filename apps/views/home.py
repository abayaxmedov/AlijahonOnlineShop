from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView

from apps.models import Category, Product, WishList, User, Order, AdminSetting


class HomeListView(ListView):
    model = Category
    template_name = 'apps/home/home.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        if self.request.user.is_authenticated:
            data['liked_products_id'] = WishList.objects.filter(user=self.request.user).values_list('product_id',
                                                                                                    flat=True)
        return data


class CompetitionListView(ListView):
    queryset = User.objects.all()
    template_name = 'apps/home/competition.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        admin = AdminSetting.objects.all().first()
        data['admin'] = admin
        return data

    def get_queryset(self):
        query = super().get_queryset()
        query = query.annotate(
            order_count=Count('owner_orders',
                              filter=Q(owner_orders__status=Order.OrderType.COMPLETED))
        ).order_by('-order_count').only('first_name')
        return query


class ThreadRequestTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/menu/thread_request.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['orders'] = Order.objects.filter(operator=self.request.user)
        return data


class DiogramTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/menu/diogram.html'
    login_url = reverse_lazy('login')
