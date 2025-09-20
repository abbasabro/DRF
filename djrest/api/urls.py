##This is Used to make the 'api/' in front of all urls
#Like this 127.0.0.1:8000/api/home/anyroute
#For this 'api/' we make this
from django.urls import path,include
urlpatterns = [
    path('home/',include('event_project.urls'))
]