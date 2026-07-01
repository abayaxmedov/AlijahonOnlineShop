from django.contrib import admin

from .models import (Product, Category, AdminSetting, Order)


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = 'slug',  'benefit'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(AdminSetting)
class AdminSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        max_instances = 1
        if self.model.objects.count() >= max_instances:
            return False
        return super().has_add_permission(request)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass