from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import UserProfile
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer

from base import mods
import re


class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})


class ChangeStyleView(APIView):
    def post(self, request):
        # validating token
        token = request.data.get('token')
        user = mods.post('authentication',
                         entry_point='/getuser/', json={'token': token})
        user_id = user.get('id', None)

        if not user_id:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        # validating style
        newstyle = request.data.get('style')
        if not newstyle in [i[0] for i in UserProfile.styles]:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        u = UserProfile.objects.get(pk=user_id)
        u.style = newstyle
        u.save(update_fields=['style'])

        return Response({})


class ChangeSexView(APIView):
    def post(self, request):
        # validating token
        token = request.data.get('token')
        user = mods.post('authentication',
                         entry_point='/getuser/', json={'token': token})
        user_id = user.get('id', None)

        if not user_id:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        # validating sex
        newsex = request.data.get('sex')
        if not newsex in [i[0] for i in UserProfile.sex_types]:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        u = UserProfile.objects.get(pk=user_id)
        u.sex = newsex
        u.save(update_fields=['sex'])

        return Response({})


class ChangeEmailView(APIView):
    def post(self, request):
        # validating token
        token = request.data.get('token')
        user = mods.post('authentication',
                         entry_point='/getuser/', json={'token': token})
        user_id = user.get('id', None)

        if not user_id:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        # validating sex
        newemail = request.data.get('email')
        if not newemail:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        u = UserProfile.objects.get(pk=user_id)
        u.email = newemail
        u.save(update_fields=['email'])

        return Response({})


class RegisterView(APIView):
    def post(self, request):

        username = request.data.get('username', '')
        sex = request.data.get('sex', '')
        email = request.data.get('email', '')
        style = request.data.get('style', '')
        pwd = request.data.get('password', '')
        if not username or not pwd or not re.match("^.{8,}$", pwd) or not sex or not style:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        if email:
            if "@" not in email:
                return Response({}, status=HTTP_400_BAD_REQUEST)

        try:
            user = UserProfile(username=username, sex=sex, style=style, email=email)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError as e:
            print(e)
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({})


class ModifyView(APIView):
    def post(self, request):
        # validating token
        token = request.data.get('token')
        user = mods.post('authentication',
                         entry_point='/getuser/', json={'token': token})
        user_id = user.get('id', None)

        if not user_id:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        u = UserProfile.objects.get(pk=user_id)

        newusername = request.data.get('username')
        u.username = newusername

        u.save(update_fields=['username'])

        print(newusername)

        return Response({})
