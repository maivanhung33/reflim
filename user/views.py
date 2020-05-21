from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view


# Create your views here.


@api_view(['POST'])
def createUser(request):
    user: dict = request.data
    if 'username' not in user.keys():
        return JsonResponse(data={'message': 'USERNAME_REQUIRE'}, status=status.HTTP_400_BAD_REQUEST)
    if 'password' not in user.keys():
        return JsonResponse(data={'message': 'PASSWORD_REQUIRE'}, status=status.HTTP_400_BAD_REQUEST)
    if 'firstName' not in user.keys():
        return JsonResponse(data={'message': 'FIRSTNAME_REQUIRE'}, status=status.HTTP_400_BAD_REQUEST)
    if 'lastName' not in user.keys():
        return JsonResponse(data={'message': 'LASTNAME_REQUIRE'}, status=status.HTTP_400_BAD_REQUEST)
    if 'email' not in user.keys():
        return JsonResponse(data={'message': 'EMAIL_REQUIRE'}, status=status.HTTP_400_BAD_REQUEST)
    existUser = User.objects.filter(username=user['username'])
    if existUser:
        return JsonResponse(data={'message': 'USER_EXISTED'}, status=status.HTTP_409_CONFLICT)
    existEmail = User.objects.filter(email=user['email'])
    if existEmail:
        return JsonResponse(data={'message': 'EMAIL_EXISTED'}, status=status.HTTP_409_CONFLICT)
    newUser = User.objects.create(username=user['username'], password=make_password(user['password']), first_name=user['firstName'], last_name=user['lastName'], email=user['email'])
    newUser.save()
    return JsonResponse(dict(id=newUser.id, username=user['username'], first_name=user['firstName'], last_name=user['lastName'], email=user['email']), status=status.HTTP_200_OK)


@api_view(['GET'])
def getUserByToken(request):
    token = request.headers['Authorization'].replace('Token ', '')
    user = Token.objects.get(key=token).user
    return JsonResponse(dict(id=user.id, username=user.username, first_name=user.first_name, last_name=user.last_name, email=user.email), status=status.HTTP_200_OK)


