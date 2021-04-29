from django.contrib import admin
from .models import *
from django.forms import ModelChoiceField, ModelForm, ValidationError
from PIL import Image


class NotebookAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Минимальное разрешение изображения - {}x{}px'.format(*Product.MIN_RESOLUTION)


    def clean_image(self):
        image = Image.open(self.cleaned_data['image'])
        
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION

        if self.cleaned_data['image'].size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения превышает 3 МБ!')

        if image.height < min_height or image.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального!')
        
        if image.height > max_height or image.width > max_width:
            raise ValidationError('Разрешение изображения больше максимального!')
        
        return self.cleaned_data['image']


class NotebookAdmin(admin.ModelAdmin):
    
    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
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