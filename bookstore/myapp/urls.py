from django.contrib import admin
from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('hello', hello),
    # path('create-category', create_category),
    # path('update-category/<pk>', update_category),
    # path('delete-category/<pk>', delete_category),
    # path('get-category-by-id/<pk>', get_category_by_id),
    # path('search-category', search_category),
    # path('get-all-category', get_all_category),
    # path('get-all-book', get_all_book),
    path('', views.index),
    path('hello2', HelloView.as_view()),
    path('category', CategoryView.as_view(), name = 'category'),
    path('book', BookView.as_view(), name = 'book'),
    path('author', AuthorView.as_view(), name = 'author'),
]