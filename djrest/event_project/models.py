from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    capacity = models.IntegerField()
    ticket_price = models.FloatField(default=100)
    status = models.CharField(max_length=255,choices=(('Upcoming','Upcoming'),('Happening','Happening'),('Cancelled','Cancelled')))
    img = models.ImageField(upload_to='images/',null=True,blank=True)

class Ticket(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=255,choices=(('VIP','VIP'),('Regular','Regular')))
    total_person = models.IntegerField(default=1)

class Booking(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=255,default='Pending')
    total_price = models.FloatField()