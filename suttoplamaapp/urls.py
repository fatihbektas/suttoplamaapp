from django.contrib import admin
from django.urls import path, include
from suttoplamaapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'suttoplamaapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('account/', include('account.urls')),
    path('mainboard/', include('mainboard.urls')),
    path('store/', include('store.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
