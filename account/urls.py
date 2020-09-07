from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('user_create/', views.register_user, name='register_user'),
    path('profile/<int:pk>/', views.detailfunc, name='account_detail'),
    # path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('login/', views.loginfunc, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'),
         name='logout'),
    path('list/', views.listfunc, name='list'),
    path('', include('shift.urls')),
]