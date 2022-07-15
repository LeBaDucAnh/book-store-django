"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from django.views.generic.base import TemplateView
from myapp import views

urlpatterns = [
    path('api/token', jwt_views.TokenObtainPairView.as_view()),
    path('signup/',views.sign_up, name='signup'),
    path('login/',views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('', views.user_main, name = 'home'),
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls'), name='api'),
    path('index/', TemplateView.as_view(template_name='pages/home.html'), name='index'),
    path('category',views.show, name="add"),
    path('<int:id>/', views.update_data, name = "update"),
    path('delete/<int:id>', views.delete_data, name = 'delete'),
    path('add', views.add_cat, name = "them"),
    path('add_author', views.add_author, name = 'add-author'),
    path('author', views.show_author, name='list'),
    path('update-author/<int:id>/', views.update_author, name = 'update-author'),
    path('delete-author/<int:id>', views.delete_author, name = 'delete-author'),
    path('add-book', views.add_book, name = 'add_book'),
    path('book', views.show_book, name='list_book'),
    path('update-book/<int:id>/', views.update_book, name = 'update_book'),
    path('delete-book/<int:id>', views.delete_book, name = 'delete_book'),
    path('detail-book/<int:id>', views.get_book_by_id, name = 'detail'),
]
