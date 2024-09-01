from django.contrib import admin

from Product.models import Product,Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    search_fields = ('name', )
    list_editable = ('is_available',)
    list_filter = ('is_available','category',)

admin.site.register(Category)
admin.site.register(Product,ProductAdmin) 