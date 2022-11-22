from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from people.views import PersonViewSet, RegisterAPIView, ImageViewSet, DocumentViewSet, ActivateUser
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'family', PersonViewSet)
router.register(r'images', ImageViewSet)
router.register(r'docs', DocumentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/token/register/', RegisterAPIView.as_view(), name='register'),
    path('accounts/activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.authtoken')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
