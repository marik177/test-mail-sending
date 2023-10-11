from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet, MailSenderViewSet, MessageViewSet, TagViewSet

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('clients', ClientViewSet)
router.register('campaigns', MailSenderViewSet)
router.register('messages', MessageViewSet)

urlpatterns = [path("", include(router.urls)), ]
