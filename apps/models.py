from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Model, CharField, ImageField, TextField, DecimalField, ForeignKey, CASCADE, DateField, \
    TextChoices, IntegerField, SET_NULL, DateTimeField, SmallIntegerField
from django.db.models.fields import BigIntegerField, SlugField
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class BaseSlugModel(Model):
    slug = SlugField(max_length=255, unique=True, blank=True, null=True)
    name = CharField(max_length=255)

    class Meta:
        abstract = True

    def save(self, **kwargs):
        slug = slugify(self.name)
        i = 1
        while Category.objects.filter(slug=slug).exists():
            slug += f"%{i}"
            i += 1 + i
        self.slug = slug
        super().save()


class CustomUserManager(UserManager):
    def _create_user(self, phone_number, password, **extra_fields):

        if not phone_number:
            raise ValueError("The given phone number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    class RoleType(TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
        OPERATOR = 'operator', 'Operator'

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    username = None
    phone_number = CharField(max_length=20, unique=True)
    district = ForeignKey('apps.District', on_delete=SET_NULL, null=True, blank=True)
    address = TextField()
    telegram_id = BigIntegerField(unique=True, blank=True, null=True)
    about = TextField(blank=True, null=True)
    role = CharField(max_length=10, choices=RoleType, default=RoleType.USER)


class Category(BaseSlugModel):
    icon = ImageField(upload_to='icons/')

    def __str__(self):
        return self.name


class Payment(Model):
    class PaymentType(TextChoices):
        REVIEW = 'review' 'Review'
        COMPLETED = 'completed', 'Complete'
        CANCEL = 'cancel', 'Cancel'

    amount = DecimalField(decimal_places=2, max_digits=12)
    photo = ImageField(upload_to='payments/')
    payment_at = DateField(auto_now_add=True)
    status = CharField(max_length=255, choices=PaymentType.choices, default=PaymentType.COMPLETED)

    user = ForeignKey('apps.User', CASCADE, related_name='payments')


class WishList(Model):
    user = ForeignKey('apps.User', CASCADE, related_name='user_wishlists')
    product = ForeignKey('apps.Product', CASCADE, related_name='product_wishlists')


class Region(Model):
    name = CharField(max_length=255)


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('apps.Region', CASCADE, related_name='districts')


class Thread(Model):
    discount_sum = DecimalField(max_digits=12, decimal_places=2)
    name = CharField(max_length=255)
    created_at = DateField(auto_now_add=True)
    visit_count = IntegerField(null=True, blank=True, default=0)

    product = ForeignKey('apps.Product', CASCADE, related_name='product_threads')
    user = ForeignKey('apps.User', CASCADE, related_name='user_threads')

    @property
    def product_price(self):
        return self.product.price - self.discount_sum


class Product(BaseSlugModel):
    description = RichTextUploadingField()
    image = ImageField(upload_to='products/')
    quantity = IntegerField()
    telegram_url = CharField(max_length=255, null=True, blank=True)

    price = DecimalField(max_digits=12, decimal_places=2)
    benefit = DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    site_sell = SmallIntegerField(default=0, null=True, blank=True)
    discount = CharField(max_length=255, null=True, blank=True)
    quantity = IntegerField(default=1)

    category = ForeignKey('apps.Category', CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Order(Model):
    class OrderType(TextChoices):
        NEW = 'new', 'New'  # yangi
        PENDING = 'pending', 'Pending'  # kutilmoqda
        READY_TO_ORDER = 'ready to order', 'Ready to order'  # buyurtma berishga tayyor
        DELIVERING = 'delivering', 'Delivering'  # Yetkazib berish
        DELIVERED = 'delivered', 'Delivered'  # Yetkazib berildi
        NOT_PICK_UP = 'not pick up', 'Not pick up'  # olmaslik
        ARCHIVED = 'archived', 'Archived'  # arxivlangan
        CANCEL = 'cancel', 'Cancel'  # Bekor qilish
        COMPLETED = 'completed', 'Completed'  # Bajarildi
        # operatorga new, pending, ready to order, archived, cancel
        # diliver delivering, delivered, not pick up, completed

    last_name = CharField(max_length=255, null=True, blank=True)
    phone_number = CharField(max_length=20)
    quantity = IntegerField(default=1)
    status = CharField(max_length=255, choices=OrderType.choices, default=OrderType.NEW)  # noqa
    order_sum = DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    ordered_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    send_date = DateField(null=True, blank=True)
    comment_operator = TextField(null=True, blank=True, default='')

    thread = ForeignKey('apps.Thread', CASCADE, related_name='thread_orders', null=True, blank=True)
    product = ForeignKey('apps.Product', CASCADE, related_name='product_orders')
    owner = ForeignKey('apps.User', CASCADE, related_name='owner_orders', null=True, blank=True)
    operator = ForeignKey('apps.User', SET_NULL, related_name='operator_orders', null=True, blank=True)
    district = ForeignKey('apps.District', SET_NULL, related_name='district_orders', null=True, blank=True)

    @property
    def amount_sum(self):
        return (self.quantity * self.product.
                price)


class AdminSetting(Model):
    # deliver_price = IntegerField()
    competition_photo = ImageField(upload_to='admin/')
    start = DateField()
    finish = DateField()
    description = RichTextUploadingField()
