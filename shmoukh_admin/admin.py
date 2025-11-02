from django.contrib import admin
from django.contrib.admin import AdminSite
from products.models import Product, ProductImage

class ShmoukhAdminSite(AdminSite):
    site_header = "Shmoukh Herbal Admin"
    site_title = "Shmoukh Administration"
    index_title = "Welcome to Shmoukh Admin Panel"

shmoukh_admin_site = ShmoukhAdminSite(name='shmoukh_admin')

@admin.register(Product, site=shmoukh_admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock_count', 'is_active']
    list_editable = ['price', 'stock_count', 'is_active']

@admin.register(ProductImage, site=shmoukh_admin_site)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text']
