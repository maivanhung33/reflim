from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from random import randint
from datetime import datetime, timezone

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from flask import Flask
from flask_mail import  Mail, Message
from user.models import RecoveryCodeUser
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
    existUser = User.objects.filter(username=user['username'], is_active=True)
    if existUser:
        return JsonResponse(data={'message': 'USER_EXISTED'}, status=status.HTTP_409_CONFLICT)
    existEmail = User.objects.filter(email=user['email'], is_active=True)
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

@api_view(['PUT'])
def updateUser(request):
    token = request.headers['Authorization'].replace('Token ', '')
    user = Token.objects.get(key=token).user
    if 'lastName' in request.data.keys():
        user.last_name = request.data['lastName']
    if 'firstName' in request.data.keys():
        user.first_name = request.data['firstName']
    user.save();
    return JsonResponse(dict(id=user.id, username=user.username, first_name=user.first_name, last_name=user.last_name, email=user.email), status=status.HTTP_200_OK)


@api_view(['POST'])
def sendRecoveryCode(request):
    if 'email' not in request.data.keys():
        return JsonResponse(data={'message': 'EMAIL_REQUIRE'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=request.data['email'], is_active=True)
    except User.DoesNotExist:
        return JsonResponse(dict(message='USER_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    code = randint(100000, 999999)
    app = Flask(__name__)
    with app.app_context():
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USE_SSL'] = False
        app.config['MAIL_USERNAME'] = "thanhsonnguyen2022@gmail.com"
        app.config['MAIL_PASSWORD'] = "Nguyenthanhson123"
        app.config['MAIL_DEFAULT_SENDER'] = "thanhsonnguyen2022@gmail.com"
        app.config['MAIL_MAX_EMAILS'] = None
        app.config['MAIL_ASCII_ATTACHMENTS'] = False
        mail = Mail(app)
        msg = Message()
        msg.subject = "Revovery code"
        msg.recipients = [request.data['email']]
        msg.sender = 'thanhsonnguyen2022@gmail.com'
        msg.body = str(code) + ' - is your Refilm account recovery code'
        mail.send(msg)
    newRecoveryCode = RecoveryCodeUser.objects.create(
        user_id=user.id,
        code=code
    )
    newRecoveryCode.save()
    return JsonResponse(dict(message='Message has been sent'), status=status.HTTP_200_OK)

@api_view(['POST'])
def forgotPasswordUser(request):
    if 'code' not in request.data.keys():
        return JsonResponse(data={'message': 'RECOVERY_CODE_REQUIRE'}, status=status.HTTP_400_BAD_REQUEST)
    if 'password' not in request.data.keys():
        return JsonResponse(data={'message': 'PASSWORD_REQUIRE'}, status=status.HTTP_400_BAD_REQUEST)
    if 'email' not in request.data.keys():
        return JsonResponse(data={'message': 'EMAIL_REQUIRE'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=request.data['email'], is_active=True)
    except User.DoesNotExist:
        return JsonResponse(dict(message='USER_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)

    try:
        recoveryCode = RecoveryCodeUser.objects.get(code=request.data['code'], user_id=user.id)
    except RecoveryCodeUser.DoesNotExist:
        return JsonResponse(dict(message='CODE_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)

    if recoveryCode.status is True:
        return JsonResponse(dict(message='CODE_USED'), status=status.HTTP_404_NOT_FOUND)
    now = datetime.now(timezone.utc)
    expired = now - recoveryCode.created_at

    if expired.total_seconds() > 300:
        return JsonResponse(dict(message='CODE_EXPIRED'), status=status.HTTP_400_BAD_REQUEST)
    user.password = make_password(request.data['password'])
    user.save()
    recoveryCode.status = True
    recoveryCode.save()
    return JsonResponse(dict(message='Change password success'), status=status.HTTP_200_OK)




