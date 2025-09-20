from django.shortcuts import render
from home.models import Student,Book
from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.serializers import *
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action,throttle_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle

#<----------Autherntication---------------->
class RegisterApi(APIView):
    def post(self,request):
      serializer = RegisterSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          return Response({
              "status" : True,
              "message" : "User Registered",
              "data": {}
          })
      return Response({
              "status" : False,
              "message" : "Error",
              "data": serializer.errors
          })
    
class LoginApi(APIView):

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username = serializer.data['username'] , 
                                password = serializer.data['password'])
            if user is None:
                return Response({
                    "status" : False,
                    "message" : "Invalid Credentials",
                    "data": {}
                },status=401)
            token,created = Token.objects.get_or_create(user=user)
            return Response({
                    "status" : True,
                    "message" : "Success",
                    "data": {
                        "token":token.key
                    }
                })
        return Response({
                    "status" : False,
                    "message" : "Invalid Data",
                    "data": serializer.errors
                })
#<----------Autherntication Ends Here---------------->   

#<--------------Viewsets------------->
from home.permissions import IsProductOwnerPermission,IsVipUser
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated , IsProductOwnerPermission , IsVipUser]
    authentication_classes = [TokenAuthentication]

    @action(detail=False,methods=['GET'])
    def export_product(self , request):
        return Response({
            "status":True,
            "message":"Record Fetched",
            "data": [] 
        })
    @action(detail=True,methods=['GET'])
    def send_email_product(self , request , pk):
        print(f'Email sent {pk}')
        return Response({
            "status":True,
            "message":f'Email sent {pk}',
            "data": [] 
        })

#<--------------Concrete View--------------->
class ProductListCreate(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class = ProductSerializer
    
#<--------------Mixins-------------->
class StudentApiMixix(ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


    # def get(self , request , *args,**kwargs):
    #     return self.list(request , *args, **kwargs)
    # def post(self , request , *args,**kwargs):
    #     return self.create(request , *args, **kwargs)
    #These Both won't work with pk URl
    
    def get(self , request , *args,**kwargs):
        return self.retrieve(request , *args, **kwargs)
    
    def put(self , request , *args,**kwargs):
        return self.update(request , *args, **kwargs)
    
    def patch(self , request , *args,**kwargs):
        return self.partial_update(request , *args, **kwargs)
    
    def delete(self , request , *args,**kwargs):
        return self.destroy(request , *args, **kwargs)
    
    #For THESE ALL Set URL With PK: 'student/<int:pk>/'

#<--------------APIVIEW------------------->    
class StudentApi(APIView):
    #It's Other Scope is in the AuthorApiV1(below)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'author'
    #Here We Overwrite the get,post,put,patch,delete methods

    def get(self , request):
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset , many = True)

        return Response({
            'status' :True,
            "message" : serializer.data,
        })
    def post(self , request):
        data = request.data
        serializer = StudentSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status': True,
                'message' : 'Records Not Created',
                'errors' : serializer.errors
            })
        serializer.save()

        return Response({
            'status': True,
            'message' : 'Records Created',
            'data' : serializer.data
        })
        
#<--------------Function Based Api(Serializers Added)---------------->
'''
Serializers Converts on form of data to another 
QuerySet--->JSON
JSON--->QuerySet
'''
#<-------------------ModelSerializer---------------->
@api_view(['GET' , 'POST' ,'PUT' ,'PATCH' , 'DELETE'])
@throttle_classes([UserRateThrottle])
def first_api(request):
    data ={
        'status':True,
        'message ' : f"Fist Api calling with {request.method}"
          }
    return Response(data)
@api_view(['POST'])
def create_records(request):
    data = request.data
    serializer = StudentSerializer(data=data)
    if not serializer.is_valid():
        return Response({
            'status': True,
            'message' : 'Records Not Created',
            'errors' : serializer.errors
        })
    serializer.save()

    return Response({
        'status': True,
        'message' : 'Records Created',
        'data' : serializer.data
    })
@api_view(['GET'])
def view_records(request):
        
    # data = [
    #     {
    #         'name' : obj.name,
    #         'mail' : obj.mail,
    #         'phone_no': obj.phone_no
    #     } 
    #     for obj in Student.objects.all()
    # ]
    queryset = Student.objects.all()
    serializer = StudentSerializer(queryset , many = True)

    return Response({
        'status' :True,
        "message" : serializer.data,
    })
@api_view(['DELETE'])
def delete_records(request,id):
    try:
        data = Student.objects.get(id=id).delete()
        return Response({
        'status': True,
        'message' : 'Records Deleted',
        'data' : data
         })  
    except Exception as e:
        return Response({
        'status': False,
        'message' : 'Records Doesnot exists',
        })
@api_view(['PATCH'])
def update_records(request):
    data = request.data
    if not data.get('id'):
        return Response({
        'status': False,
        'errors' : 'ID required',
        })
    
    student = Student.objects.get(id=data.get('id'))
    serializer = StudentSerializer(student , data=data , partial = True)
    if not serializer.is_valid():
        return Response({
            'status': True,
            'message' : 'Records Not Updated',
            'errors' : serializer.errors
        })
    serializer.save()
    return Response({
        'status': True,
        'message' : 'Records updated',
        'data' : serializer.data
    })  

#<-------------------ModelSerializer ends here---------------->  

#<--------------Basic Serializer------------------------>
@api_view(['POST'])
def create_book(request):
    data = request.data
    serializer = NewBookSerializer(data=data)
    if not serializer.is_valid():
        return Response({
            'status': True,
            'message' : 'Records Not Created',
            'errors' : serializer.errors
        })
    print(serializer.validated_data)
    serializer.save()

    return Response({
        'status': True,
        'message' : 'Records Created',
        'data' : serializer.data
    })  

@api_view(['GET'])
def view_book(request):
    queryset = Book.objects.all()
    serializer = CreateBookSerializer(queryset , many = True)
    return Response({
        'status' :True,
        "message" : serializer.data,
    })     

@api_view(['POST'])
def create_user(request):
    data = request.data
    serializer = UserSerializer(data=data)
    if not serializer.is_valid():
        return Response({
            'status': True,
            'message' : 'Records Not Created',
            'errors' : serializer.errors
        })
    print(serializer.validated_data)
    #serializer.save()

    return Response({
        'status': True,
        'message' : 'Records Created',
        'data' : serializer.data
    })  


#<-------------For Paginator----------------------->
#1.PageNumberPagination
#2.CursorPagination(Secure URL from webScrappers)
from utils.paginate import LargeResultsSetPaginator,StandardResultsSetPaginator,CustomCursorPagination,paginate
from django.core.paginator import Paginator
from utils.throttle import CustomThrottle

class AuthorApi(APIView):
    throttle_classes = [AnonRateThrottle,CustomThrottle] 
    def get(self,request):
        querset = Author.objects.all()
        paginator = CustomCursorPagination()
        paginated_results = paginator.paginate_queryset(querset,request)
        serializer = AuthorSerializer(paginated_results,many=True)
        return Response(
            paginator.get_paginated_response(serializer.data).data
        )
    
class AuthorMixin(ListModelMixin,GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = StandardResultsSetPaginator #same used in Viewsets
    
    def get(self , request , *args,**kwargs):
        return self.list(request , *args, **kwargs)
   
class AuthorApiV1(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'author'
    def get(self,request):
        querset = Author.objects.all()
        pagenumber = request.GET.get('page',1)
        paginator = Paginator(querset,10)
        data = paginate(querset,paginator,pagenumber)
        serializer = AuthorSerializer(data['results'],many=True)
        data['results'] = serializer.data

        return Response( data)
       