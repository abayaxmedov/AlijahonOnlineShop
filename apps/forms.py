import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.forms import CharField, IntegerField
from django.forms.forms import Form

from apps.models import User, Order


class LoginForm(Form):
    phone_number = CharField(max_length=255)
    password = CharField(max_length=255)

    # check_box = BooleanField(error_messages={"required" : "Shartlarni qabul qiling !"})

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        return "+" + re.sub('\D', "", phone_number)

    def clean_password(self):
        return make_password(self.cleaned_data.get('password'))


class ProfileForm(LoginRequiredMixin, Form):
    first_name = CharField(required=False)
    last_name = CharField(required=False)
    district_id = CharField(required=False)
    address = CharField(required=False)
    telegram_id = IntegerField(required=False)
    about = CharField(required=False)

    def update(self, user):
        data = {key: values for key, values in self.cleaned_data.items() if values not in [None, ""]}
        if data:
            User.objects.filter(pk=user.pk).update(**data)


class PasswordUpdateForm(Form):
    old = CharField(required=False)
    new = CharField(required=False)
    confirm = CharField(required=False)

    def clean_new(self):
        return make_password(self.cleaned_data.get('new'))

    def clean_confirm(self):
        new = self.data.get('new')
        confirm = self.cleaned_data.get('confirm')
        if new != confirm:
            raise ValidationError("Parollar mos emas")

    def update(self, user):
        password = self.cleaned_data.get('new')
        User.objects.filter(pk=user.id).update(password=password)


class OrderForm(Form):
    last_name = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    product_id = IntegerField()

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        return "+" + re.sub('\D', "", phone_number)



    def save(self, user):
        return Order.objects.create(**self.cleaned_data, owner=user)