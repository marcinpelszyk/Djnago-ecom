from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .utils import get_or_set_order_session

from .models import Product



class ProductListView(ListView):
    queryset = Product.products.all()
    template_name = 'cart/product_list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name= 'cart/product_detail.html'
    context_object_name = 'product'