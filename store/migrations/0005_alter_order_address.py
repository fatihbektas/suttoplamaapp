# Generated by Django 4.2.6 on 2023-11-12 22:44

from django.db import migrations
import mapbox_location_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=mapbox_location_field.models.LocationField(map_attrs={'center': [38.59821903435276, 27.350622679963262], 'placeholder': 'Haritadan konum seçiniz.'}, null=True, verbose_name='Siparişin Konumu'),
        ),
    ]
