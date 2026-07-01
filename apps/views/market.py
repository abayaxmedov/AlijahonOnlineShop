from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView

from apps.forms import ThreadFrom
from apps.models import Product, Category, Thread


class MarketListView(LoginRequiredMixin, ListView):
    queryset = Product.objects.all()
    template_name = 'apps/market/market-list.html'
    context_object_name = 'products'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        products = Product.objects.all()
        slug = self.kwargs.get('slug')
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        query  = self.requqest.GET.get('query')
        if query:
            products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if slug != 'all':
            products = products.filter(category__slug=slug)
        if slug == 'top':
            products = Product.objects.annotate(order_count=Count(F('product_orders'))).order_by('-order_count')
        data['products'] = products
        return data

class ThreadFormView(FormView):
    form_class = ThreadFrom
    template_name = 'apps/market/market-list.html'
    success_url = reverse_lazy('thread-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        data['categories'] = Category.objects.all()
        return data

    def form_valid(self, form):
        pass
        thread = form.save(commit=False)
        thread.user = self.request.user
        thread.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        pass
        for message in form.errors.values():
            messages.error(self.request, message)
        return super().form_invalid(form)


class ThreadListView(ListView):
    queryset = Thread.objects.all()
    template_name = 'apps/market/thread-list.html'
    context_object_name = 'threads'

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        data['threads'] = Thread.objects.filter(user=self.request.user).order_by('-created_at')
        return data



class ThreedProductDetailView(DetailView):
    queryset = Thread.objects.all()
    template_name = "apps/order/detail.html"
    context_object_name = "threed"

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        data["product"] = data.get("threed").product
        data.get("threed").visit_count += 1
        data.get("threed").save()
        return data
