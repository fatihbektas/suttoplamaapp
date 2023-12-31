# Generated by Django 4.2.6 on 2023-11-03 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='person-circle.svg', null=True, upload_to='')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('date_ordered', models.DateTimeField(auto_now_add=True, null=True)),
                ('complete', models.BooleanField(default=False, null=True)),
                ('status', models.CharField(choices=[('Recived', 'Sipariş alındı'), ('Pending', 'İşlem görüyor'), ('Assigned', 'Servise atandı'), ('Delivered', 'Teslim edildi')], default='Sipariş alındı', max_length=20, null=True)),
                ('note', models.CharField(max_length=500, null=True)),
                ('assign_date', models.DateTimeField(null=True, verbose_name='Servise atama tarihi')),
                ('service_date', models.DateTimeField(null=True, verbose_name='Servise başlama tarihi')),
                ('delivery_date', models.DateTimeField(null=True, verbose_name='Teslim tarihi')),
                ('service_time', models.IntegerField(default=0)),
                ('delivery_time', models.IntegerField(default=0)),
                ('is_delivered', models.BooleanField(default=False, null=True, verbose_name='Teslimat')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.customer')),
            ],
            options={
                'ordering': ['-date_ordered'],
                'permissions': (('is_operator', 'Operator yetkisine sahip'), ('is_service', 'Servis görevlisi yetkisine sahip')),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.service'),
        ),
    ]
