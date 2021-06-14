from django import forms
from django import forms
from .models import OrderItem


class AddCartForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = ['quantity']

