from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app.views import MotoRetrieveView, YachtRetrieveView
from rent_telegram_bot import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('moto/', MotoRetrieveView.as_view(), name='moto'),
    path('yacht/', YachtRetrieveView.as_view(), name='yacht'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
