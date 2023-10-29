from django.db import models
from django.urls import reverse

class Order(models.Model):
    def get_absolute_url(self):
        return reverse("store:detail", kwargs={"id": self.id})
    
