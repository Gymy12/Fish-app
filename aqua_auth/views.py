from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.http import HttpRequest
from .models import CustomerUser, Gender, UserTypes


def signin(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
    return render(request, "login.html")


def signup(request: HttpRequest):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        gender = Gender.objects.filter(id=gender).first()

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e)
            return render(request, "register.html")

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, e)
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "register.html")

        if CustomerUser.objects.filter(email=email).exists():
            messages.error(request, "User already exists, try logging in")
            return render(request, "register.html")

        user = CustomerUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
            phone=phone,
            gender=gender,
            password=password,
            user_type=UserTypes.objects.get(id=2),
        )
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred")
    genders = Gender.objects.all()
    print(genders)
    return render(
        request,
        "register.html",
        {"genders": genders},
    )


def signout(request: HttpRequest):
    logout(request)
    return redirect("home")


def profile(request: HttpRequest):
    return render(request, "profile.html")


def change_password(request: HttpRequest):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        user = request.user
        if user.check_password(current_password):
            if new_password == confirm_password:
                try:
                    validate_password(new_password)
                except ValidationError as e:
                    messages.error(request, e)
                    return render(request, "change_password.html")
                user.set_password(new_password)
                user.save()
                login(request, user)
                messages.success(request, "Password changed successfully")
                return redirect("profile")
            else:
                messages.error(request, "Passwords do not match")
                return render(request, "change_password.html")
        else:
            messages.error(request, "Invalid password")
            return render(request, "change_password.html")
    return render(request, "change_password.html")


def update_profile(request: HttpRequest):
    if request.method == "POST":
        phone = request.POST.get("phone")

        user = request.user
        user.phone = phone
        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect("profile")
