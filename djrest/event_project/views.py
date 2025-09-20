from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from event_project.models import *
from event_project.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from event_project.permission import IsAdminUser
from rest_framework.decorators import action
from django.db.models import Q

class RegisterApi(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":True,
                "message":"User Created Successfully",
                "data":{}
            })
        return Response({
                "status":False,
                "message":"Error",
                "data":serializer.errors
            })
    
class LoginApi(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data['username'],
                                password=serializer.data['password'])
            if user is None:
                return Response({
                "status":False,
                "message":"Invalid Credentials",
                "data":serializer.errors
                },status=401)
            token,created = Token.objects.get_or_create(user=user)
            return Response({
                "status":True,
                "message":"Login SuccessFully",
                "data":{
                    'token':token.key
                }
            })
        
class PublicEventViewset(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get'] #Disabling Create Update delete methods

    @action(detail=False,methods=['GET'])
    def search_event(self,request):
        search=request.GET.get('search')
        events=Event.objects.all()
        if search:
            events =events.filter(Q(title__icontains =search) |Q(description__icontains =search))
        serializer = EventSerializer(events,many=True)
        return Response({
            "status":True,
            "message":"Record Fetched",
            "data": serializer.data
        })
        
class PrivateEventViewset(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @action(detail=False,methods=['GET'])
    def get_booking(self,request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings,many=True)
        return Response({
            "status":True,
            "message":"Booking Fetcehd",
            "data": serializer.data
            })

    @action(detail=False,methods=['POST'])
    def create_booking(self,request):
        data= request.data
        serializer = TicketBookingSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
            "status":True,
            "message":"Booking done",
            "data": serializer.data
            })
        return Response({
            "status":False,
            "message":"Booking Failed",
            "data": serializer.errors
            })