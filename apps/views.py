from django.shortcuts import render
from django.views.generic import TemplateView


class AuthTemplateView(TemplateView):
    template_name = 'apps/auth/auth.html'
