from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView

from apps.forms import OrderModelForm
from apps.models import Order, Category, Region


class OperatorTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/operator/operator-page.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        status = self.request.GET.get('status')
        category_id = self.request.GET.get('category_id')
        district_id = self.request.GET.get('district')
        user_role ={
            'operator' : ['new', 'pending', 'cancel', 'not pick up', 'archived']
        }
        data['categories'] = Category.objects.all()
        data['regions'] = Region.objects.all()
        orders = Order.objects.all()
        if status:
            if status == 'new':
                orders = orders.filter(status=status)
            else:
                orders = orders.filter(operator=self.request.user, status=status)

        if category_id:
            orders = orders.filter(product__category__slug=category_id)
        if district_id:
            orders = orders.filter(district_id=district_id)
        data['status'] = user_role.get(self.request.user.role)
        data['orders'] = orders
        return data


class OperatorOrderDetailView(DetailView):
    queryset = Order.objects.all()
    template_name = 'apps/operator/operator-order-change.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        order_id = self.kwargs.get('pk')
        Order.objects.filter(pk=order_id).update(operator=self.request.user)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['regions'] = Region.objects.all()
        return data


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderModelForm
    template_name = 'apps/operator/operator-order-change.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('operator')
