from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView

from apps.forms import OrderForm
from apps.models import Product, AdminSetting, Order, Thread


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "apps/order/detail.html"
    slug_url_kwarg = "slug"
    context_object_name = "product"


class OrderFormView(FormView):
    form_class = OrderForm
    template_name = 'apps/order/detail.html'
    success_url = reverse_lazy('order')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['threads'] = Thread.objects
        return data

    def form_valid(self, form):
        pass
        form.cleaned_data['owner_id'] = self.request.user.id
        price = Product.objects.filter(pk=form.cleaned_data['product_id']).first().price
        deliver_price = AdminSetting.objects.first().deliver_price
        form.cleaned_data['order_sum'] = deliver_price + price
        thread_id = form.cleaned_data.get('thread_id')
        if thread_id:
            benefit = Thread.objects.filter(pk=thread_id).first().product.benefit
            form.cleaned_data['order_sum'] = deliver_price + price - benefit
        order = form.save()
        return render(self.request, 'apps/order/success.html', context={"order": order, "deliver_price": deliver_price})

    def form_invalid(self, form):
        pass


class OrderListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    queryset = Order.objects.all()
    template_name = 'apps/order/order-list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(owner_id=self.request.user.id)
