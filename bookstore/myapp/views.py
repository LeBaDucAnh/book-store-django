from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from datetime import datetime
from django.db.models import Q
from .models import *
from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from .form import SignUpForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filter import *


# Create your views here.

def index(request):
    return render(request, "pages/home.html")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hello(request):
    return Response({"message": "Hello world!"})


class HelloView(APIView):
    permission_classes = [IsAuthenticated]

    def get (request):
        return Response({"message": "Hello"})


class CategorySerializer(forms.ModelForm):
    class Meta:
        paginate_by = 2
        model = Category
        fields = '__all__'
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'category_name': forms.TextInput(attrs={'class': 'form-control'})
        }


class BookSerializer(forms.ModelForm):
    class Meta:
        paginate_by = 2
        model = Book
        fields = '__all__'
        widgets = {
            'code' : forms.TextInput(attrs = {'class':'form-control'}),
            'book_name': forms.TextInput(attrs={'class': 'form-control'}),
            'total_qty': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_price': forms.TextInput(attrs={'class': 'form-control'}),
            'published_year': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class AuthorSerializer(forms.ModelForm):
    class Meta:
        paginate_by = 2
        model = Author
        fields = '__all__'
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'author_image': forms.ImageField()
        }


class CategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = [Category.category_name for Category in Category.objects.all()]
        return Response(result)

    def post(self, request):
        try:
            data = request.data
            Category.objects.create(
                code=data['code'],
                category_name=data['category_name']
            )
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})

    def put(self, request, pk):
        try:
            data = request.data
            category = Category.objects.get(pk=pk)
            category.code = data['code']
            category.category_name = data['category_name']
            category.save()

            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})


class BookView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        book_list = Book.objects.all()
        data = BookSerializer(book_list, many=True).data
        return Response(data)

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def put(self, request, pk):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(data=request.data, instance=Book)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})


class AuthorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        author_list = Author.objects.all()
        data = AuthorSerializer(author_list, many=True).data
        return Response(data)

    def post(self, request, format=None):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def put(self, request, pk):
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(data=request.data, instance=Author)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
            author.delete()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})


# @api_view(['GET'])
# def get_all_category(requests):
#     cat_list = Category.objects.all()
#     result = CategorySerializer(cat_list, many=True).data
#     return Response(result)
#
#
# @api_view(['POST'])
# def create_category(request):
#     serializer = CategorySerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors, status=400)
#
#     # try:
#     #     data = request.data
#     #     Category.objects.create(
#     #         code = data['code'],
#     #         category_name=data['category_name']
#     #     )
#     #     return Response({'success': True})
#     # except Exception as e:
#     #     return Response({'success': False, 'error': str(e)})
#
#
# @api_view(['PUT'])
# def update_category(request, pk):
#     category = Category.objects.get(pk=pk)
#     serializer = CategorySerializer(data=request.data, instance=Category)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors, status=400)
#
#     # try:
#     #     data = request.data
#     #     category = Category.objects.get(pk=pk)
#     #     category.code = data['code']
#     #     category.category_name = data['category_name']
#     #     category.save()
#     #
#     #     return Response({'success': True})
#     # except Exception as e:
#     #     return Response({'success': False, 'error': str(e)})
#
#
# @api_view(['DELETE'])
# def delete_category(request, pk):
#     try:
#         category = Category.objects.get(pk=pk)
#         category.delete()
#         return Response({'success': True})
#     except Exception as e:
#         return Response({'success': False, 'error': str(e)})
#
#
# def model_to_dict(category):
#     return {
#         'category_name': category.category_name,
#         'code': category.code
#     }


@api_view(['GET'])
def get_category_by_id(request, pk):
    category = Category.objects.get(pk=pk)
    data = CategorySerializer(Category).data
    return Response(data)

    # try:
    #     category = Category.objects.get(pk=pk)
    #     return Response(model_to_dict(category))
    # except Exception as e:
    #     return Response({'success': False, 'error': str(e)})


@api_view(['GET'])
def search_category(request):
    keyword = request.GET.get('keyword', '')
    category_list = Category.objects.filter(
        Q(category_name__icontains=keyword) |
        Q(code__icontains=keyword)
    )
    result = CategorySerializer(category_list, many=True).data
    # result = [model_to_dict(category) for category in category_list]
    return Response(result)


# @api_view(['GET'])
# def get_all_book(requests):
#     book_list = Book.objects.all()
#     result = BookSerializer(book_list, many=True).data
#     return Response(result)
#
#
# @api_view(['POST'])
# def create_book(request):
#     serializer = BookSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors, status=400)
def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account Created Successfully!!!')
            fm.save()
    else:
        fm = SignUpForm()
    return render(request, 'registration/signup.html', {'form': fm})


# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!!!')
                    return HttpResponseRedirect('/index/')
        else:
            fm = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': fm})
    else:
        return HttpResponseRedirect()


def user_main(request):
    if request.user.is_authenticated:
        return render(request, 'pages/home.html', {'name': request.user})
    else:
        return HttpResponseRedirect('/login/')


# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def add_cat(request):
    if request.method == 'POST':
        fm = CategorySerializer(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['code']
            em = fm.cleaned_data['category_name']
            reg = Category(code=nm, category_name=em)
            reg.save()
            fm = CategorySerializer()
            return HttpResponseRedirect('/category')
    else:
        fm = CategorySerializer()
    return render(request, 'pages/add.html', {'form': fm})


def show(request):
    contact_list = Category.objects.all()
    myFilter = CategoryFilter(request.GET, queryset=contact_list)
    contact_list = myFilter.qs
    paginator = Paginator(contact_list, 10)  # Show 25 contacts mỗi page

    page_number = request.GET.get("page")
    try:
        contacts = paginator.get_page(page_number)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'pages/list_view.html', {'contacts': contacts, 'myFilter': myFilter})


# edit and update function
def update_data(request, id):
    if request.method == 'POST':
        pi = Category.objects.get(pk=id)
        fm = CategorySerializer(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/category')
    else:
        pi = Category.objects.get(pk=id)
        fm = CategorySerializer(instance=pi)
    return render(request, 'pages/update.html', {'form': fm})


# delete function
def delete_data(request, id):
    if request.method == 'POST':
        pi = Category.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/category')


# for author

def add_author(request):
    if request.method == 'POST':
        fm = AuthorSerializer(request.POST, request.FILES)
        if fm.is_valid():
            nm = fm.cleaned_data['author_name']
            em = fm.cleaned_data['author_image']
            reg = Author(author_name=nm, author_image=em)
            reg.save()
            fm = AuthorSerializer()
            return HttpResponseRedirect('/author')
    else:
        fm = AuthorSerializer()
    return render(request, 'pages/author/add.html', {'form': fm})


def show_author(request):
    contact_list = Author.objects.all()
    myFilter = AuthorFilter(request.GET, queryset=contact_list)
    contact_list = myFilter.qs
    paginator = Paginator(contact_list, 10)  # Show 25 contacts mỗi page

    page_number = request.GET.get("page")
    try:
        contacts = paginator.get_page(page_number)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'pages/author/list.html', {'contacts': contacts, 'myFilter': myFilter})


# edit and update function
def update_author(request, id):
    if request.method == 'POST':
        pi = Author.objects.get(pk=id)
        fm = AuthorSerializer(request.POST, request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/author')
    else:
        pi = Author.objects.get(pk=id)
        fm = AuthorSerializer(instance=pi)
    return render(request, 'pages/author/update.html', {'form': fm})


# delete function
def delete_author(request, id):
    if request.method == 'POST':
        pi = Author.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/author')


# book

def add_book(request):
    if request.method == 'POST':
        fm = BookSerializer(request.POST, request.FILES)
        if fm.is_valid():
            cd = fm.cleaned_data['code']
            bkname = fm.cleaned_data['book_name']
            total = fm.cleaned_date['total_qty']
            unit = fm.cleaned_data['unit_price']
            year = fm.cleaned_data['published_year']
            publish = fm.cleaned_data['publisher']
            anh = fm.cleaned_data['image']
            des = fm.cleaned_data['description']
            tacgia = fm.cleaned_data['author']
            theloai = fm.cleaned_data['category']
            reg = Book(code=cd, book_name=bkname, total_qty = total, unit_price = unit, published_year = year, publisher = publish, image = anh, description = des, author = tacgia, category = theloai)
            reg.save()
            fm = BookSerializer()
            return HttpResponseRedirect('/book')
    else:
        fm = BookSerializer()
    return render(request, 'pages/books/add.html', {'form': fm})


def show_book(request):
    contact_list = Book.objects.all()
    myFilter = BookFilter(request.GET, queryset=contact_list)
    contact_list = myFilter.qs
    paginator = Paginator(contact_list, 10)  # Show 25 contacts mỗi page

    page_number = request.GET.get("page")
    try:
        contacts = paginator.get_page(page_number)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'pages/books/list.html', {'contacts': contacts, 'myFilter': myFilter})


# edit and update function
def update_book(request, id):
    if request.method == 'POST':
        pi = Book.objects.get(pk=id)
        fm = BookSerializer(request.POST, request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/book')
    else:
        pi = Book.objects.get(pk=id)
        fm = BookSerializer(instance=pi)
    return render(request, 'pages/books/update.html', {'form': fm})


# delete function
def delete_book(request, id):
    if request.method == 'POST':
        pi = Book.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/book')


def get_book_by_id(request, id):
    book = Book.objects.get(pk=id)
    data = BookSerializer(book).data
    return render(request, 'pages/books/detail.html', {'data':data})
