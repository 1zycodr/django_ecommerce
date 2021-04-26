from django.contrib import admin
from .models import *
from django.forms import ModelChoiceField


class NotebookAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(db_field)
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'), label='Категория')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(db_field)
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'), label='Категория')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)