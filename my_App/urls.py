from . import views
from django.urls import path
from django.contrib.auth import views as auth_views



urlpatterns = [
   
    path('calculator/', views.calculator, name='calculator'),  # Home page (index.html)
    # urls.py
   path('result/<int:metrics_id>/', views.result_view, name='result'),  # Only keep this one
    path('registerUser/', views.registerUser, name='registerUser'),
    path('login/', views.login, name='login'),
     path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html',
             email_template_name='password_reset_email.html',
             subject_template_name='password_reset_subject.txt'
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    path('logout/', views.logout, name='logout'),
    path('my-account/', views.my_account, name='myAccount'),
    path('edit-profile/', views.edit_profile, name='editProfile'),
    path('health-history/', views.health_history, name='healthHistory'),
    path('download-results/', views.download_results, name='downloadResults'),
    path('change-password/', views.change_password, name='changePassword'),
    path('delete-account/', views.delete_account, name='deleteAccount'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('health/chart/', views.health_chart_view, name='healthChart'),

]