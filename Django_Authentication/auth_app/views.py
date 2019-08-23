from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
from auth_app.models import UserDetailModel


def login(request):
    if request.method != "POST":
        return HttpResponse(" INVALID REQUEST METHOD")
    else:
        try:
            input = request.POST["input"]
            password = request.POST["password"]
            if UserDetailModel.objects.get(phone=input).exists():
                obj = UserDetailModel.objects.get(phone=input)
            elif UserDetailModel.objects.get(email=input).exists():
                obj = UserDetailModel.objects.get(email=input)
            else:
                return HttpResponse("User Does not exist")

            if check_password(password, obj.password):

                return HttpResponse("Authenticated")
            else:
                return HttpResponse("Incorrect Credentials")
        except Exception as e:
            return HttpResponse(str(e))


def create_user(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        UserDetailModel.objects.create(first_name=first_name,
                                       last_name=last_name,
                                       email=email,
                                       phone=phone,
                                       password=make_password(password))
        return HttpResponse("success")
    else:
        return HttpResponse("..........")
