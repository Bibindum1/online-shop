from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Category, Product, ProductGallery


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
    fields = ['image', 'alt_text', 'is_main']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_active', 'created_at', 'view_details']
    inlines = [ProductGalleryInline]
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    list_editable = ['price', 'is_active']

    def view_details(self, obj):
        url = reverse('catalog:product_detail_admin', kwargs={'pk': obj.pk})
        return format_html(
            '<a class="button" href="{}">Детали</a>',
            url
        )

    view_details.short_description = 'Просмотр'
