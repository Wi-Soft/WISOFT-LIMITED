from django.contrib import admin

from .models import Category, Product, StockMovement, PortfolioRating, CustomerOrder, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'stock', 'is_low_stock', 'image_preview')
    list_filter = ('category',)
    search_fields = ('name', 'sku', 'barcode', 'description')
    readonly_fields = ('image_preview',)
    fields = (
        'name', 'sku', 'barcode', 'category', 'description',
        'price', 'stock', 'low_stock_alert', 'image', 'image_preview',
    )

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="height:70px;object-fit:cover;border-radius:6px">', obj.image.url)
        return 'No image uploaded'

    image_preview.short_description = 'Image Preview'


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'created_at')
    list_filter = ('movement_type',)


@admin.register(PortfolioRating)
class PortfolioRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user__username', 'comment')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'total_amount')


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'full_name', 'phone', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'full_name', 'phone', 'address')
    inlines = [OrderItemInline]