import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.forms import CharField, IntegerField, DecimalField, ModelForm
from django.forms.forms import Form

from .models import User, Order, Thread, Product


class LoginForm(Form):
    phone_number = CharField(max_length=255)
    password = CharField(max_length=255)

    # check_box = BooleanField(error_messages={"required" : "Shartlarni qabul qiling !"})

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        return "+" + re.sub(r'\D', "", phone_number)

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
    first_name = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    product_id = IntegerField()
    thread_id = IntegerField(required=False)
    owner_id = IntegerField(required=False)
    order_sum = DecimalField(max_digits=12, decimal_places=2, required=False)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        return "+" + re.sub(r'\D', "", phone_number)

    def save(self):
        return Order.objects.create(**self.cleaned_data)


class ThreadFrom(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False


    class Meta:
        model = Thread
        fields = 'name', 'discount_sum', 'product', 'user'

    def clean_discount_sum(self):
        pass
        product_id = self.data.get('product')
        product = Product.objects.filter(pk=product_id).first()
        discount_sum = self.cleaned_data.get('discount_sum')
        if discount_sum == "Yo'q":
            discount_sum = 0
        if product.benefit < discount_sum:
            raise ValidationError("Chegirma miqdoridan ko'p")
        return discount_sum



class OrderModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment_operator'].required = False

    class Meta:
        model = Order
        fields = 'quantity', 'send_date', 'district' ,'status', 'comment_operator'
