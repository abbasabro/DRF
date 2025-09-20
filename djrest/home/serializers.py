'''
Used to Convert/Translate 
objects -> JSON
JSON -> Objects
'''

from rest_framework import serializers
from home.models import *
from datetime import datetime
from .validators import no_name
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255,validators=[no_name])
    password = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("UserName Already Exists")
        return username
    
    def create(self, validated_data):
        username = validated_data['username']
        password= validated_data['password']
        first_name= validated_data['first_name']
        last_name= validated_data['last_name']

        user = User.objects.create_user(
            username=username , password=password , first_name=first_name , last_name=last_name
        )
        
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255,validators=[no_name])
    password = serializers.CharField(max_length=255)

    
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def calculate_age(self, date_of_birth):
        current_date = datetime.now()
        age = current_date.year -  date_of_birth.year 
        return age
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['age'] = self.calculate_age(instance.dob)
        return data
    
    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        student.student_id = f"STU-{student.id}".zfill(5)
        student.save()
        return student
    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'name' in data:
            data['name'] = data['name'].strip().title()
            print(data['name'])

        return data
    
    def get_fields(self):
        data = super().get_fields()
        authenticated = False
        if authenticated:
            data = data['email'].pop()
            
        return(data)

from rest_framework.validators import UniqueValidator
class BookSerializer(serializers.Serializer):
    book_title = serializers.CharField(max_length=100 , validators = [UniqueValidator(queryset=Book.objects.all())])
    author = serializers.CharField(max_length=50)
    price = serializers.FloatField()
    TAX_PRICE = 5

    def calculate_tax_price(self,price):
        return self.TAX_PRICE + price
    def to_representation(self, instance):
        book = {
            "book_title":instance.book_title,
            "author":instance.author,
            "price":self.calculate_tax_price(instance.price)
            
        }
        return book

    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        return book
    
    def update(self, instance, validated_data):
        book_title = validated_data.get('book_title' , instance.book_title)
        author = validated_data.get('author' , instance.author)
        price = validated_data.get('price' , instance.price) 

        instance.book_title = book_title
        instance.author = author
        instance.price = price
        instance.save()

        return instance
    
class AddressSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=100)
    postal_code = serializers.CharField()

    def validate_postal_code(self,value):
        if not value.isdigit():
            raise serializers.ValidationError('Postal Code Should be digit')
        return value
            
class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100 , validators = [no_name])
    email = serializers.EmailField()
    age = serializers.IntegerField()
    phone_no = serializers.RegexField(
        regex=r'^03[0-9]{9}$',error_messages = {
            'invalid' : 'Phone Number Must be in correct format'
        }
    )

    address = AddressSerializer()
    user_type = serializers.ChoiceField(['admin' , 'regular'])
    admin_code = serializers.CharField(required=False)

    #Below Both Validation in a single function
    def validate(self, data):
        if 'age' in data and data['age'] < 18 or data['age']  > 30:
            raise serializers.ValidationError("Age must be above 18 and below 30")

        if 'email' in data and data['email'].split('@')[1]=='gmail.com':
            raise serializers.ValidationError("Only accept Bussines email")  
        if data['user_type'] == 'admin'  and not data.get('admin_code') :
            raise serializers.ValidationError("Admin Code is required")
        return super().validate(data)
        
    
    # def validate_age(self, value):
    #     if value < 18 or value > 30:
    #         raise serializers.ValidationError("Age must be above 18 and below 30")     
    #     return value
    # def validate_email(self, value):
    #     if value.split('@')[1]=='gmail.com':
    #         raise serializers.ValidationError("Only accept Bussines email")     
    #     return value
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'
class NewBookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    publishers = PublisherSerializer(many = True)
    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        publisher_datas = validated_data.pop('publishers')
        author , _ = Author.objects.get_or_create(**author_data)
        book = Book.objects.create(author=author , **validated_data)
        for publisher_data in publisher_datas:
            publisher ,_ = Publisher.objects.get_or_create(**publisher_data)
            book.publishers.add(publisher)
        return book

class CreateBookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset = Author.objects.all())
    publishers = serializers.PrimaryKeyRelatedField(queryset = Publisher.objects.all(),many=True)
    class Meta:
        model = Book
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
