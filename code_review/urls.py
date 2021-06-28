import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import TransferViewSet, UserProfileSet
from app import views

router = DefaultRouter()
router.register(r'transfer', TransferViewSet, basename='transfer')
router.register(r'profile', UserProfileSet, basename='profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', views.TransferView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]
urlpatterns += router.urls
