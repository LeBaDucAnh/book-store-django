from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.fullname

    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def does_exits(self):
        return Customer.objects.filter(email=self.email)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username


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

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    qty = models.IntegerField()
    price_unit = models.IntegerField()
    total = models.IntegerField()
    order_date = models.DateTimeField()
    deliver_date = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()




