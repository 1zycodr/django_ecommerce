from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import *
from .mixins import CategoryDetailMixin, CartMixin 

class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'categories': Category.objects.get_categories_for_left_sidebar(), 
            'products': LatestProducts.objects.get_products_for_main_page('notebook', 'smartphone', with_respect_to='notebook'),
        }
        return render(request, 'base.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):
    
    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook, 
        'smartphone': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart, 
            'categories': Category.objects.get_categories_for_left_sidebar()
        }
        return render(request, 'cart.html', context)