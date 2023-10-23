from django.urls import path
from mainboard import views

app_name = 'mainboard'

urlpatterns = [
    path("", views.mainboard, name="mainboard"),
    path("user/", views.user_page, name="user_page"),
    path("service/", views.service_page, name="service_page"),
    path("account/", views.account_settings, name="account"),
    path("customer/<str:pk>/", views.view_customer, name="customer"),
    path("chart", views.view_chart, name="chart"),
]
