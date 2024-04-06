from django.shortcuts import render, redirect
from .models import SubscribedUsers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactForm
from .models import Image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserChangeForm, ImageForm
from django.conf import settings
import requests



def home_page(request):
    return render(request, "website/index.html")


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send email
            send_mail(
                subject,
                f"From: {name} <{email}>\n\n{message}",
                'alexkinyua001alx@gmail.com',
                ['alexkinyua001alx@gmail.com'], 
                fail_silently=False,
            )
            messages.success(request, 'Thank you for the feedback. We will keep in touch!!')
        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        form = ContactForm()

    return render(request, "website/contact_us.html", {'form': form})


def gallery(request):
    images = Image.objects.all()  # Fetch all images from the database
    return render(request, "website/gallery.html", {'images': images})



def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)

        if not email:
            messages.error(request, "You must type an email to subscribe to a Newsletter")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request, "Email address is already subscribed.")
            return redirect(request.META.get("HTTP_REFERER", "/"))  

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")

        subscribe_model_instance = SubscribedUsers()
        subscribe_model_instance.email = email
        subscribe_model_instance.save()
        messages.success(request, f'{email} email was successfully subscribed to our newsletter!')
        return redirect(request.META.get("HTTP_REFERER", "/"))
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('account')
        else:
            # Return an invalid login error message.
            return render(request, 'website/login.html', {'error': 'Invalid credentials!! Try again.'})
    else:
        return render(request, 'website/login.html')
    



@login_required
def account(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'website/account.html', {'form': form})

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")



@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Updating the session with the new password hash
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'website/account.html', {'form': form})


def add_picture_to_gallery(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.errors)
            messages.success(request, 'Picture added to gallery successfully.')
            return redirect('account')
        
    else:
        form = ImageForm()
    return render(request, 'website/account.html', {'form': form})