from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "Twoje imię"
    }))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "Twój adres email"
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Wiadomość"
    }))