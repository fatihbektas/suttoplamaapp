from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from store.models import Customer, Order

# Yeni bir kullanıcı varsayılan olarak 'customer' grubuna atanır


def customer_user_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )
        print('Kullanıcı oluşturuldu')


post_save.connect(customer_user_profile, sender=User,
                  dispatch_uid='customer_user_profile')
