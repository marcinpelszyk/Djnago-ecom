from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


from .models import Product



class ProductListView(ListView):
    queryset = Product.products.all()
    template_name = 'cart/product_list.html'

class ProductDetailView(DetailView):
    model = Product
    template_name=''
