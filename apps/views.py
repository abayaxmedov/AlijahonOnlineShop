from unicodedata import category

from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView, DetailView

from apps.forms import LoginForm, ProfileForm, PasswordUpdateForm, OrderForm
from apps.models import User, Category, Region, Product, District, WishList


# Create your views here.


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'apps/auth/login.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        data = form.cleaned_data
        phone_number = data.get("phone_number")
        password = form.data.get("password")
        hash_password = data.get("password")
        query_set = User.objects.filter(phone_number=phone_number)
        if query_set.exists():
            user = query_set.first()
            if user.check_password(password):
                login(self.request, user)
            else:
                messages.error(self.request, "Parol xato !")
                return redirect('login')
        else:
            user = User.objects.create(password=hash_password, phone_number=phone_number)
            login(self.request, user)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "\n".join([error[0] for error in form.errors.values()]))
        return super().form_invalid(form)


class ProfileFormView(LoginRequiredMixin, FormView):
    form_class = ProfileForm
    template_name = 'apps/auth/profile.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['regions'] = Region.objects.all()
        return data

    def form_valid(self, form):
        form.update(self.request.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        pass


class ProfileUserTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'apps/auth/profile-user.html'


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class HomeListView(ListView):
    model = Category
    template_name = 'apps/home/home.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        if self.request.user.is_authenticated:
            data['liked_products_id'] = WishList.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        return data


def get_districts(request):
    region_id = request.GET.get('region_id')
    districts = District.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)


class PasswordUpdateFormView(FormView):
    form_class = PasswordUpdateForm
    template_name = 'apps/auth/profile.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        pass
        session_password = self.request.user.password
        old_password = form.cleaned_data.get('old')
        if not check_password(old_password, session_password):
            messages.error(self.request, "Old password not much!")
            return self.render_to_response(self.get_context_data(form=form))
        else:
            form.update(self.request.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for message in form.errors.values():
            messages.error(self.request, message)
        return redirect('profile')


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/menu/product-list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        category = Category.objects.filter(slug=slug).first()
        data = super().get_context_data(**kwargs)
        if slug != 'all':
            data['products'] = Product.objects.filter(category=category)
        data['categories'] = Category.objects.all()
        if self.request.user.is_authenticated:
            data['liked_products_id'] = WishList.objects.filter(user=self.request.user).values_list('product_id', flat=True)
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


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "apps/order/detail.html"
    slug_url_kwarg = "slug"
    context_object_name = "product"


class LikeListView(ListView):
    queryset = WishList.objects.all()
    template_name = 'apps/menu/wish-list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.filter(product_wishlists__user=self.request.user)
        if self.request.user.is_authenticated:
            data['liked_products_id'] = WishList.objects.filter(user_id=self.request.user).values_list('product_id', flat=True)
        return data


class OrderFormView(FormView):
    form_class = OrderForm
    success_url = reverse_lazy('order')

    def form_valid(self, form):
        order = form.save(self.request.user)
        return render(self.request, 'apps/order/order-success.html', context={"order":order})

    def form_invalid(self, form):
        pass