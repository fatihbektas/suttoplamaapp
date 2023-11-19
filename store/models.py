from django.db import models
from django.contrib.auth.models import User
from django.db.models import Func, F, Sum
from django.urls import reverse
from mapbox_location_field.models import LocationField


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(
        default='person-circle.svg', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(null=True, blank=True)

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name


class Service(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    ORDER_STATUS = (
        ('Recived', 'Sipariş alındı'),
        ('Assigned', 'Servise atandı'),
        ('Transporting', 'Taşımada'),
        ('Delivered', 'Teslim edildi'),
    )
    transaction_id = models.CharField(max_length=200, null=True)
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    status = models.CharField(max_length=20, null=True,
                              choices=ORDER_STATUS, default='Sipariş alındı')
    note = models.CharField(max_length=500, null=True)
    assign_date = models.DateTimeField(
        verbose_name='Servise atama tarihi', null=True)
    service_date = models.DateTimeField(
        verbose_name='Servise başlama tarihi', null=True)
    delivery_date = models.DateTimeField(
        verbose_name='Teslim tarihi', null=True)
    service_time = models.IntegerField(default=0)
    delivery_time = models.IntegerField(default=0)
    is_delivered = models.BooleanField(
        verbose_name='Teslimat', default=False, null=True, blank=False)
    address = LocationField(verbose_name='Siparişin Konumu', null=True, blank=False, map_attrs={
                            'placeholder': 'Haritadan konum seçiniz.',
                            'center': [38.59821903435276, 27.350622679963262],
                            })

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total_price = float(sum([item.get_total for item in order_items]))
        return total_price

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total_item = sum([item.quantity for item in order_items])
        return total_item

    def get_absolute_url(self):
        return reverse('store:detail', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('store:update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('store:delete', kwargs={'id': self.id})

    def get_assign_url(self):
        return reverse('store:assign', kwargs={'id': self.id})

    def get_service_url(self):
        return reverse('store:service', kwargs={'id': self.id})

    def get_delivery_url(self):
        return reverse('store:delivery', kwargs={'id', self.id})

    class Meta:
        ordering = ['-date_ordered']
        permissions = (
            ('is_operator', 'Operator yetkisine sahip'),
            ('is_service', 'Servis görevlisi yetkisine sahip'),
        )


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return super().__str__()
