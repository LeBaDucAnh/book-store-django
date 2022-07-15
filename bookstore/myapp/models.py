from django.db import models

# Create your models here.
class Employees(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.fullname


# class User(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=100)
#     fullname = models.CharField(max_length=100)
#     phone = models.CharField(max_length=15)
#     email = models.CharField(max_length=50)
#     birthday = models.DateField()
#     address = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.fullname


class Author(models.Model):
    author_name = models.CharField(max_length=50)
    author_image = models.ImageField(upload_to='static/images/author', blank=True)

    def __str__(self):
        return self.author_name


class Category(models.Model):
    code = models.CharField(max_length=20, unique=True)
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class Book(models.Model):
    code = models.CharField(max_length=20, unique=True)
    book_name = models.CharField(max_length=100)
    total_qty = models.IntegerField()
    unit_price = models.IntegerField()
    published_year = models.IntegerField()
    publisher = models.CharField(max_length=50)
    image = models.ImageField(upload_to='static/images/book')
    description = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.book_name

class Order(models.Model):
    class OrderStatus:
        PENDING = 0
        DELIVERED = 1
        CANCELED = 2

    #customer = models.ForeignKey(User, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    qty = models.IntegerField()
    price_unit = models.IntegerField()
    total = models.IntegerField()
    order_date = models.DateTimeField()
    deliver_date = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()




