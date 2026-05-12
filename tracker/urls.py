"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register_view, name='register'),

    path('login/', views.login_view, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('add-expense/', views.add_expense, name='add_expense'),

    path('edit-expense/<int:id>/', views.edit_expense, name='edit_expense'),

    path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),

    path('logout/', views.logout_view, name='logout'),

    path('add-income/', views.add_income, name='add_income'),

    path('profile/', views.profile, name='profile'),

    path('upload-profile-photo/', views.upload_profile_photo, name='upload_profile_photo'),

]