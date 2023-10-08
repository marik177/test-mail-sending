from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, ClientViewSet, \
    MailSenderViewSet, MessageViewSet

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('clients', ClientViewSet)
router.register('campaigns', MailSenderViewSet)
router.register('messages', MessageViewSet)

urlpatterns = [path("", include(router.urls)), ]
