from django.urls import path
from .views import index, ProductDetailView

urlpatterns = [
    path('', index, name='base'),
    path('products/<str:ct_model>/<str:slug>', ProductDetailView.as_view(), name='product_detail')
]