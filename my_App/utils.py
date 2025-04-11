
# configures user detection

from django.shortcuts import redirect


def detectUser(user):
    if user.is_superadmin:
        # Redirect to admin panel if the user is an admin
        return redirect('/admin')
    
    elif user.role == 1:
        # If the role is 'Customer' (1), redirect to customer dashboard
        return redirect('calculator')
    
    # Default case for invalid roles or other users
    return redirect('/login')
    
   
