# from django import forms 
# from .models import User



# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     confirm_password = forms.CharField(widget=forms.PasswordInput())
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']
    
    
#     def clean(self):
#         cleaned_data = super(UserForm, self).clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
        
#         if password != confirm_password:
#             raise forms.ValidationError(
#                 'Password does not match!'
#             )
            

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile

class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=11, required=True)
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2', 'profile_picture')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'address_line_1', 'address_line_2', 
                 'city', 'state', 'country', 'pin_code')