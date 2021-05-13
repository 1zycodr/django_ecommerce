from django.shortcuts import redirect, render, HttpResponseRedirect
from django.views.generic import DetailView, View
from django.contrib import messages
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['ct_model'] = self.model._meta.model_name
        return context


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


class AddProductToCartView(CartMixin, View):
    
    def get(self, request, *args, **kwargs):
        
        ct_model = kwargs.get('ct_model') 
        slug = kwargs.get('slug')

        product = ContentType.objects.get(model=ct_model).model_class().objects.get(slug=slug)

        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, 
            cart=self.cart, 
            object_id=product.id, 
            content_type=ContentType.objects.get(model=ct_model)
        )

        if created:
            self.cart.products.add(cart_product)
        else:
            cart_product.quantity += 1
            cart_product.save()

        cart_data = self.cart.products.aggregate(models.Sum('final_price'), models.Sum('quantity'))

        if cart_data.get('final_price__sum') is not None:
            self.cart.final_price = cart_data.get('final_price__sum')
        else: 
            self.cart.final_price = 0

        self.cart.total_products = cart_data.get('quantity__sum')
        self.cart.save()

        messages.add_message(request, messages.INFO, "Товар добавлен!")

        return HttpResponseRedirect('/cart')


class ChangeQuantityView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        if request.POST.get('quantity'):
            ct_model = kwargs.get('ct_model') 
            slug = kwargs.get('slug')

            product = ContentType.objects.get(model=ct_model).model_class().objects.get(slug=slug)

            cart_product = CartProduct.objects.get(
                user=self.cart.owner, 
                cart=self.cart, 
                object_id=product.id, 
                content_type=ContentType.objects.get(model=ct_model)
            )

            cart_product.quantity = int(request.POST.get('quantity'))
            cart_product.save()

            cart_data = self.cart.products.aggregate(models.Sum('final_price'), models.Sum('quantity'))

            if cart_data.get('final_price__sum') is not None:
                self.cart.final_price = cart_data.get('final_price__sum')
            else: 
                self.cart.final_price = 0

            self.cart.total_products = cart_data.get('quantity__sum')
            self.cart.save()

            messages.add_message(request, messages.INFO, "Количество изменено!")
            

        return HttpResponseRedirect('/cart')


class DeleteFromCart(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model = kwargs.get('ct_model') 
        slug = kwargs.get('slug')

        product = ContentType.objects.get(model=ct_model).model_class().objects.get(slug=slug)

        cart_product = CartProduct.objects.get(
            user=self.cart.owner, 
            cart=self.cart, 
            object_id=product.id, 
            content_type=ContentType.objects.get(model=ct_model)
        )

        self.cart.products.remove(cart_product)
        cart_product.delete()

        cart_data = self.cart.products.aggregate(models.Sum('final_price'), models.Sum('quantity'))

        if cart_data.get('final_price__sum') is not None:
            self.cart.final_price = cart_data.get('final_price__sum')
        else: 
            self.cart.final_price = 0

        self.cart.total_products = cart_data.get('quantity__sum')
        self.cart.save()

        messages.add_message(request, messages.INFO, "Товар удалён!")

        return HttpResponseRedirect('/cart')