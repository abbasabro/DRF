
from django.urls import path
from event_project.views import *
from rest_framework.routers import DefaultRouter

#Model ViewSet Routes
router = DefaultRouter()
router.register(r'private/event',PrivateEventViewset,basename="private-event")
router.register(r'public/event',PublicEventViewset,basename="public-event")
router.register(r'booking',BookingViewSet,basename="booking")

urlpatterns = [
    path('register/',RegisterApi.as_view()),
    path('login/',LoginApi.as_view())
    
]
urlpatterns +=router.urls
