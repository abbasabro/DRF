from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ExtendedUser(models.Model):
    user = models.OneToOneField(User,related_name='extended',on_delete=models.CASCADE)
    is_vip = models.BooleanField(default=False)
class Student(models.Model):
    student_id = models.CharField(null=True,blank=True)
    name = models.CharField()
    mail = models.EmailField()
    dob = models.DateField(null=True,blank=True)
    phone_no = models.IntegerField()

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()

    def __str__(self):
        return self.name
    
class Book(models.Model):
    book_title = models.CharField(max_length=100,unique=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True,blank=True , related_name="publisher_book")
    publishers = models.ManyToManyField(Publisher,related_name="books")

    def __str__(self):
        return self.book_title

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)