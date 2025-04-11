from . import views
from django.urls import path



urlpatterns = [
   
    path('calculator/', views.calculator, name='calculator'),  # Home page (index.html)
    path('result/', views.result, name='result'),  # Result page (result.html)
    path('registerUser/', views.registerUser, name='registerUser'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('dashboard/', views.dashboard, name='dashboard'),
]