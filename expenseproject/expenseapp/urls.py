from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='expenseapp/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_expense, name='add_expense'),
    path('add-category/', views.add_category, name='add_category'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),
]