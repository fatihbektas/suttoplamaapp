from django.contrib import admin
from django.urls import path, include
from suttoplamaapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('account/', include('account.urls')),
    path('mainboard/', include('mainboard.urls')),
    path('store/', include('store.urls')),
]
