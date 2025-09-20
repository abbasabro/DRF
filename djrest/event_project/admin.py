from django.contrib import admin
from event_project.models import *
# Register your models here.
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Booking)