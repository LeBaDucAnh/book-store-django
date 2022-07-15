from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Employees)
# admin.site.register(User)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Order)
