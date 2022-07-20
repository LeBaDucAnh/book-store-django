import django_filters
from django_filters import CharFilter
from .models import *
from django import forms
class CategoryFilter(django_filters.FilterSet):
    category_name = CharFilter(field_name="category_name", lookup_expr='icontains')
    class Meta:
        model = Category
        fields = ['category_name']
        widgets = {
            'category_name': forms.TextInput(attrs={'title':'abc'})
        }


class AuthorFilter(django_filters.FilterSet):
    author_name = CharFilter(field_name="author_name", lookup_expr='icontains')
    class Meta:
        model = Author
        fields = ['author_name']

class BookFilter(django_filters.FilterSet):
    # code = CharFilter(field_name="code", lookup_expr='code')
    book_name = CharFilter(field_name="book_name", lookup_expr='icontains')
    # unit_price = CharFilter(field_name="unit_price", lookup_expr='icontains')
    # published_year = CharFilter(field_name="published_year", lookup_expr='icontains')
    # publisher = CharFilter(field_name="publisher", lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['book_name']


class CustomerFilter(django_filters.FilterSet):
    fullname = CharFilter(field_name="fullname", lookup_expr='icontains')
    class Meta:
        model = Customer
        fields = ['fullname']