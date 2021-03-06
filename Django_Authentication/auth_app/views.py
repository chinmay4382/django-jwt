import json
import pickle

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
from Django_Authentication import settings
from auth_app.models import UserDetailModel
import jwt

import hashlib


# def generate_token(payload: dict):
#     return jwt.encode(payload, settings.TOKEN_KEY, algorithm='HS256').decode("utf-8")


def send_response_raw_json(response_object, http_status=200):
    response_object["check_token"] = hashlib.md5(pickle.dumps(response_object)).hexdigest()
    token = jwt.encode(response_object, settings.TOKEN_KEY, algorithm='HS256').decode("utf-8")
    r_o = {"token": token}
    json_object = json.dumps(r_o, skipkeys=True, indent=2, cls=DjangoJSONEncoder)

    return HttpResponse(json_object, content_type='application/json', status=http_status)


def login(request):
    if request.method != "POST":
        return HttpResponse(" INVALID REQUEST METHOD")
    else:
        try:
            input = request.POST["input"]
            password = request.POST["password"]
            if UserDetailModel.objects.filter(phone=input).exists():
                obj = UserDetailModel.objects.get(phone=input)
            elif UserDetailModel.objects.filter(email=input).exists():
                obj = UserDetailModel.objects.get(email=input)
            else:
                return HttpResponse("User Does not exist")
            obj.created_on = str(obj.created_on)
            obj.updated_by = str(obj.updated_by)
            obj.is_delete = str(obj.is_delete)
            if check_password(password, obj.password):
                obj_dict = obj.__dict__
                obj_dict.pop("_state")
                return send_response_raw_json(obj_dict)
            else:
                return HttpResponse("Incorrect Credentials")
        except Exception as e:
            return HttpResponse(str(e))


def check_with_token(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        token = jwt.decode(request.META['HTTP_AUTHORIZATION'],settings.TOKEN_KEY)
        hashed_token = token["check_token"]
        token.pop("check_token")
        if hashed_token== hashlib.md5(pickle.dumps(token)).hexdigest():
            json_obj = json.dumps(token, indent=2, cls=DjangoJSONEncoder)

            return HttpResponse(json_obj)
    else:
        return HttpResponse("Permisiion Denied")


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
        return HttpResponse("Something went wrong Please Try once again")
