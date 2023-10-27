from django.urls import path
from store import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name='store'),
    path('shopping-cart/', views.shopping_cart, name='shopping-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item/', views.update_item, name='update_item'),
]
