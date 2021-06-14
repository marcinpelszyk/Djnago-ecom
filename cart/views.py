from django.forms import forms
from django.shortcuts import render, get_list_or_404
from django.views import generic
from django.urls import reverse
from .utils import get_or_set_order_session

from .models import Product
from .forms import AddCartForm



class ProductListView(generic.ListView):
    queryset = Product.products.all()
    template_name = 'cart/product_list.html'

class ProductDetailView(generic.FormView):
    template_name= 'cart/product_detail.html'
    form_class = AddCartForm


    def get_object(self):
        return get_list_or_404(Product, slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse('home') # cart

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object()

        item_filter = order.items.filter(product=product)

        if item_filter.exists():
            item = item_filter.first()
            item.quantity = int(form.cleaned_data['quantity'])

        else:
            new_item = forms.save(commit=False)
            new_item.product = product
            new_item.order = order
            new_item.save()

        return super(ProductDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["products"] = self.get_object()
        return context


        