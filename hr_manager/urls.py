from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

import hr.views as views
import catalog.views as catalog_views


router = routers.DefaultRouter()
router.register(r'register', views.RegisterViewSet, 'register')
router.register(r'products', catalog_views.ProductViewSet, 'products')

urlpatterns = [
    # Website Pages
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('employers/', views.employers_view, name='employers'),
    path('upload/', views.upload_view, name='upload'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # API Paths
    path('api/', include(router.urls)),
    path('api/auth/', jwt_views.TokenObtainPairView.as_view(), name='api-auth'),
    path('api/auth/refresh/', jwt_views.TokenRefreshView.as_view(), name='api-auth-refresh'),

    # Utility Views
    path('sendemail/', views.send_email_view, name='sendemail'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
