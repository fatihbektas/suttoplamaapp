from django.urls import path
from store import views

app_name = 'store'

urlpatterns = [
    path('', views.store, name='store'),
    path('shopping-cart/', views.shopping_cart, name='shopping-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item/', views.update_item, name='update-item'),

    path('delete-order/<int:id>/', views.order_delete, name='delete'),
    path('<int:id>/detail/', views.order_detail, name='detail'),
    path('<int:id>/assing/', views.order_assign, name='assign'),
    path('<int:id>/assing/<int:sid>/',views.order_assign_to_service, name='assign_to_service'),
    path('<int:id>/assign/service/', views.order_service, name='service'),
    path('<int:id>/assign/delivery/', views.order_delivery, name='delivery'),
]
