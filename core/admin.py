from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'stock', 'is_featured', 'get_image', 'created_at']
    list_filter = ['category', 'is_featured']
    search_fields = ['name', 'description']
    list_editable = ['price', 'discount_price', 'stock', 'is_featured']
    fields = ['name', 'description', 'price', 'discount_price', 'image', 'image_url', 'stock', 'category', 'is_featured', 'get_image_display']
    readonly_fields = ['get_image_display']

    def get_image_display(self, obj):
        """
        Display the resolved image URL (from get_image property) in the admin.
        """
        return obj.get_image
    get_image_display.short_description = "Image URL"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'total_price']
    search_fields = ['user__username']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    search_fields = ['product__name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status']
    search_fields = ['user__username', 'transaction_id']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['product__name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']  # Fixed: Removed space in 'list display'
    list_filter = ['rating']
    search_fields = ['product__name', 'user__username']