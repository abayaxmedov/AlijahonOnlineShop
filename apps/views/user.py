from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView
from apps.forms import LoginForm, ProfileForm, PasswordUpdateForm
from apps.models import User, Region, District


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
    login_url = reverse_lazy('login')



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
