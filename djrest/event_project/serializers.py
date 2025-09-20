from rest_framework import serializers
from event_project.models import *
from django.contrib.auth.models import User
from django.db.models import Sum

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username Already Exists")
        return username
    
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']

        user = User.objects.create_user(
            username=username,password=password,first_name=first_name,last_name=last_name
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=255)
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
    #For Getting the ticket Details
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['event'] = EventSerializer(instance.ticket.event).data
        response['ticket'] = TicketSerializer(instance.ticket).data
        return response
    
class TicketBookingSerializer(serializers.Serializer):
    event = serializers.IntegerField()
    ticket_type = serializers.CharField()
    total_person = serializers.IntegerField()
    user = serializers.IntegerField()

    def validate_event(self,value):
        if not Event.objects.filter(id=value , status ="Happening").exists():
            raise serializers.ValidationError("Event does not exists.")
        return value
    
    def validate_user(self,value):
        if not Event.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exists.")
        return value
    
    def validate(self, data):
        event = Event.objects.get(id=data['event'])
        total_person = data['total_person']
        ticket_limit = event.capacity
        total_count = Ticket.objects.aggregate(generated_tickets=Sum("total_person"))
        generated_tickets = total_count['generated_tickets']
        print(generated_tickets)
        if total_person >= ticket_limit:
            raise serializers.ValidationError(f"Limit Seat : {ticket_limit}")
        if generated_tickets:
            if generated_tickets >= ticket_limit:
                raise serializers.ValidationError(f"Sold OUT!!")
        return data


    def create(self, validated_data):
        event = Event.objects.get(id=validated_data['event'])
        user = User.objects.get(id=validated_data['user'])
        total_person = validated_data['total_person']
        ticket_type = validated_data['ticket_type']
        ticket = Ticket.objects.create(
            event = event ,
            ticket_type = ticket_type,
            total_person = total_person
        )
        total_price = event.ticket_price * total_person
        booking = Booking.objects.create(
            ticket=ticket,
            user=user,
            status='Paid',
            total_price=total_price
        )
        return {
            "event":event.id,
            "ticket_type":ticket_type,
            "total_person":total_person,
            "user":user.id
        }