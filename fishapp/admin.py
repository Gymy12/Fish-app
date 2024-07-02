from django.contrib import admin
from .models import Banner, Category,Product,Quantity,ProductAttribute
from .models import Count

admin.site.register(Quantity)
admin.site.register(Count)



class BannerAdmin(admin.ModelAdmin):
    list_display=('alt_text','image_tag')
admin.site.register(Banner, BannerAdmin)   




class CategoryAdmin(admin.ModelAdmin):
    list_display=('title', 'image_tag')
admin.site.register(Category, CategoryAdmin)    




class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'get_quantity_unit','count','price', 'is_featured','status')
    list_editable = ('status', 'is_featured')

    def get_quantity_unit(self, obj):
        return obj.quantity.get_unit_display()
    get_quantity_unit.short_description = 'Quantity Unit'
admin.site.register(Product, ProductAdmin)    




class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag','product','get_quantity_unit','count','price')

    def get_quantity_unit(self, obj):
        return obj.quantity.get_unit_display()
    get_quantity_unit.short_description = 'Quantity Unit'
admin.site.register(ProductAttribute, ProductAttributeAdmin)    