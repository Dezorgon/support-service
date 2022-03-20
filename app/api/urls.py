from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import (GetMessageViewSet, MessageViewSet, TicketViewSet,
                       UserViewSet, spam_email)


router = routers.SimpleRouter()
router.register('tickets', TicketViewSet)
router.register(r'tickets/(?P<ticket_pk>[^/.]+)/messages', GetMessageViewSet, basename='message')
router.register('messages', MessageViewSet)
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('spam_email/', spam_email),
] + router.urls
