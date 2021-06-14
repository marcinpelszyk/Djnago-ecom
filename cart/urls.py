from django.urls import path
from .views import ProductListView 

app_name = 'cart'

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),    
]
