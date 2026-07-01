from django.views.generic import TemplateView


class TestTemplateView(TemplateView):
    template_name = 'apps/order/'