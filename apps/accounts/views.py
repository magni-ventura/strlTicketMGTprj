"""
This module contains the views for the customer account section of the website.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from.form import RegisterCustomerForm
from.models import *

# Register a customer
User = get_user_model()

def register_customer(request):
    """
    This function registers a new customer account.
    """
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            # save the form data to the database
            var = form.save(commit=False)
            var.is_customer = True
            var.username = var.email
            var.save()
            messages.success(request, 'Your Account Has Been Successfully Registered. Please Login to continue')
            return redirect ('login')
        else:
            messages.warning(request, 'Something Went Wrong. Please Check Form Inputs for Error and Try Again')
            return redirect ('register-customer')
    else:
        form = RegisterCustomerForm()
        context = {'form':form}
        return render(request, 'accounts/register_customer.html', context)



# Log in User
def login_user(request):
    """
    This function logs in a user.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please Check Form Input')
            return redirect ('login')
    else:
        return render(request, 'accounts/login.html')


# Log out User
def logout_user(request):
    """
    This function logs out a user.
    """
    logout(request)
    messages.success(request, 'Your Active Session Has Ended. Please Login To Continue')
    return redirect ('login')

#change password - in app
#update Profile