from django.contrib import admin
from home.models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Product)
admin.site.register(ExtendedUser)

