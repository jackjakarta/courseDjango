from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib.auth import logout, get_user_model
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Employer
from .forms import UserImageForm, RegisterForm
from .serializers import RegisterSerializer


AuthUserModel = get_user_model()


def home_view(request):
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


def contact_view(request):
    return render(request, "contact.html", {
        "message": "This is a dynamic message."
    })


def employers_view(request):
    all_employers_qs = Employer.objects.all()
    print(all_employers_qs)
    return render(request, "employers.html", {
        "message": "Dynamic message!",
        "employers": all_employers_qs
    })


def upload_view(request):
    if request.method == "GET":
        form = UserImageForm()
    else:
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "You're file has been uploaded successfully!")
            return redirect("home")

    return render(request, "upload.html", {
        "form": form
    })


def send_email_view(request):
    first_employer = Employer.objects.first()

    context = {
        "first_name": "John",
        "last_name": "McDonald",
        "company": first_employer.name
    }

    template = get_template("email/email.html")
    content = template.render(context)
    mail = EmailMultiAlternatives(
        subject="Your account has been registered.",
        body=content,
        to=["alex.termure@yahoo.com"]
    )
    mail.content_subtype = "html"
    mail.send()
    messages.success(request, "You're email has been sent.")
    return redirect("home")


def register_view(request):
    if request.method == "GET":
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have registered successfully!")
            return redirect("home")

    return render(request, "register.html", {
        "form": form
    })


class RegisterViewSet(viewsets.ViewSet):
    @staticmethod
    def create(request):
        user = request.user
        register_serializer = RegisterSerializer(data=request.POST)

        if register_serializer.is_valid():
            register_serializer.create(register_serializer.validated_data)

            content = {
                "message": "User was created successfully!"
            }

            return Response(content, status=200)

        return Response(register_serializer.errors, status=400)

    @staticmethod
    def list(request):
        all_users = AuthUserModel.objects.all()
        register_serializer = RegisterSerializer(all_users, many=True)

        content = {
            "users": register_serializer.data,
        }

        return Response(content, status=200)
