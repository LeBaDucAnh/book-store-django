from django.contrib.auth.handlers.modwsgi import check_password
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from datetime import datetime
from django.db.models import Q
from .models import *
from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from .form import *
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filter import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
import re
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

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

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

class CustomerSerializer(forms.ModelForm):
    class Meta:
        paginate_by = 2
        model = Customer
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),

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

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'registration/profile.html', {'user_form':user_form, 'profile_form':profile_form})



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
    paginator = Paginator(contact_list, 10)  # Show 25 contacts m???i page

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
    paginator = Paginator(contact_list, 10)  # Show 25 contacts m???i page

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
    paginator = Paginator(contact_list, 10)  # Show 25 contacts m???i page

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


def search(request):
    if request.method == "POST":
        q = request.POST['q']
        books = Book.objects.filter(Q(book_name__icontains=q)|Q(unit_price__icontains = q)|Q(code__icontains = q))
        return render(request, 'pages/books/search.html', {'q':q, 'books':books})
    else:
        return render(request, 'pages/books/search.html', {})


# customers


def add_customer(request):
    if request.method == 'POST':
        fm = CustomerSerializer(request.POST, request.FILES)
        if fm.is_valid():
            user = fm.cleaned_data['username']
            passw = fm.cleaned_data['password']
            fname = fm.cleaned_data['fullname']
            phone = fm.cleaned_data['phone']
            mail = fm.cleaned_data['email']
            address = fm.cleaned_data['address']

            reg = Customer(username=user, password=passw, fullname=fname, phone=phone, email=mail, address=address)
            reg.save()
            fm = CustomerSerializer()
            return HttpResponseRedirect('/customer')
    else:
        fm = CustomerSerializer()
    return render(request, 'pages/customers/add.html', {'form': fm})


def show_customer(request):
    contact_list = Customer.objects.all()
    myFilter = CustomerFilter(request.GET, queryset=contact_list)
    contact_list = myFilter.qs
    paginator = Paginator(contact_list, 10)  # Show 25 contacts m???i page

    page_number = request.GET.get("page")
    try:
        contacts = paginator.get_page(page_number)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'pages/customers/list.html', {'contacts': contacts, 'myFilter': myFilter})


# edit and update function
def update_customer(request, id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        fm = CustomerSerializer(request.POST, request.FILES, instance=pi)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/customer')
    else:
        pi = Customer.objects.get(pk=id)
        fm = CustomerSerializer(instance=pi)
    return render(request, 'pages/customers/update.html', {'form': fm})


# delete function
def delete_customer(request, id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/customer')


def login(request):
    if request.method == "GET":
        return render(request, 'users/login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_msg = None
        if customer:
            #flag = check_password(password, customer.password)
            if password == customer.password:
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email
                return redirect("index/users")
            else:
                error_msg = "Email or Password is incorrect."
        else:
            error_msg = "Email is incorrect."
        return render(request, 'users/login.html', {'error_msg': error_msg})

def homePage(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    context = {'books': books, 'categories': categories}
    return render(request, 'users/home.html', context)

def basePgae(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    context = {'books': books, 'categories': categories}
    return render(request, 'users/base.html', context)

# def add_to_cart(request):
#     return render(request, 'users/home.html', {'contact_list': contact_list})


def signup(request):
    if request.method == 'GET':
        return render(request, 'users/signup.html')
    else:
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer(fullname=fullname, phone=phone, email=email, password=password)

        values = {
            'fullname': fullname,
            'phone': phone,
            'email': email,
        }

        err_msg = None
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pas = re.compile(reg)
        mat = re.search(pas, password)
        if not fullname:
            err_msg = "Full Name Required."
        elif len(fullname) < 5:
            err_msg = "Full Name must be 5 characters long."
        elif not phone:
            err_msg = "Phone is Required."
        elif len(phone) < 10:
            err_msg = "Phone Number must be 10 characters long."
        elif not email:
            err_msg = "Email is Required."
        elif not password:
            err_msg = "Password is Required"
        elif not mat:
            err_msg = "Password is invalid"
        elif customer.does_exits():
            err_msg = "User with this email address already registered."
        if not err_msg:
            customer.save()
            return redirect('index/users')
        else:
            return render(request, 'users/signup.html', {'error_msg': err_msg, 'values': values})

@login_required(login_url="user-login")
def logout(request):
    request.session.clear()
    return redirect('user-login')

def cart(request):
    cart_product_id = list(request.session.get('cart').keys())
    cart_product = Book.get_products_by_id(cart_product_id)
    print(cart_product)
    return render(request, 'users/cart.html')


def homePage(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('index/users')

    else:
        products = None
        categories = Category.objects.all()
        category_id = request.GET.get('category')
        if category_id:
            products = Book.objects.filter(category=category_id)
        else:
            products = Book.objects.filter(category=1)
        context = {'products': products, 'categories': categories}
        print("Your Email Address is: ", request.session.get('email'))
        return render(request, 'users/home.html', context)