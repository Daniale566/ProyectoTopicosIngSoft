from django.contrib import admin
from .models import Gafas, Order

@admin.register(Gafas)
class GafasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock')
    search_fields = ('nombre',)
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
    ordering = ('-created_at',)
    fields = ('user', 'gafas', 'address', 'payment_method', 'status')
    readonly_fields = ('user', 'gafas', 'address', 'payment_method', 'created_at', 'total_price')

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'