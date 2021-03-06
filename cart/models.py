from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.expressions import F
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse

User = get_user_model()


class ProductMenager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)



class Address(models.Model):
    ADDRESS_CHOICES = (
        ('B', 'Billing'),
        ('S', 'Shipping'),
    )


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line_1}, {self.address_line_2}, {self.city}"

    class Meta:
        verbose_name_plural = 'Addresses'

class Product(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    image = models.ImageField(upload_to='product_images')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    objects = models.Manager()
    products = ProductMenager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        
        return reverse('cart:product-detail', args=[self.slug])

class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} X {self.product}"


        

   
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)


    billing_address = models.ForeignKey(
        Address, related_name='billing_address', blank=True, null=True, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', blank=True, null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"Zam??wienie-{self.pk}"




class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=(
        ('PayPal', 'PayPal'),
    ))
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    amount = models.FloatField()
    # PayPal API
    raw_response = models.TextField()


    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"P??atno????-{self.order}-{self.pk}"
    


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.titile)

pre_save.connect(pre_save_product_receiver, sender=Product)
