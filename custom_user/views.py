import json
import os
import sys

from rest_framework import generics, status, permissions, exceptions
from rest_framework.response import Response
from .serializer import UserBaseSerializer, RegisterFormSerializer, LoginFormSerializer, User


class AuthRegister(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        try:
            request_serializer = RegisterFormSerializer(data=request.data)
            request_serializer.is_valid(raise_exception=True)
            user = User(
                email=request_serializer.validated_data['email'],
                first_name=request_serializer.validated_data['first_name'],
                last_name=request_serializer.validated_data['last_name'],
                username=request_serializer.validated_data['username'],
                is_active=False,
                profile_image=request_serializer.validated_data[
                    'profile_image'] if request_serializer.validated_data.get('profile_image') else None
            )
            user.set_password(request_serializer.validated_data['password'])
            user.save()
            user_serializer = UserBaseSerializer(user)
            result = {'user': user_serializer.data}
            return Response(data=result, status=status.HTTP_201_CREATED)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)


class AuthLogin(generics.GenericAPIView):
    serializer_class = LoginFormSerializer

    def post(self, request, *args, **kwargs):
        request_serializer = LoginFormSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        print("request", request_serializer.data)
        user = User.objects.filter(username=request_serializer.validated_data['username']).first()
        print(user)
        if user and user.check_password(request_serializer.validated_data['password']) and user.is_active:
            print("user login ")
            user_serializer = UserBaseSerializer(user)
            if user.is_superuser:
                all_users = User.objects.all().exclude(username=user.username)
                list_user = []
                for usr in all_users:
                    usr_serializer = UserBaseSerializer(usr)
                    list_user.append(usr_serializer.data)
                result = {"user": user_serializer.data, "user_details": list_user, "is_admin": True}
            else:
                result = {'user': user_serializer.data}
            return Response(data=result, status=status.HTTP_200_OK)
        else:
            print("exception", request_serializer.errors)
            raise exceptions.AuthenticationFailed()


class DeleteUser(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        request_data = request.data
        print(request_data)
        user_id = request_data['user_id']
        user = User.objects.filter(id=user_id).first()
        try:
            print(user)
            deleted_user = user.delete()

            result = {"status": "success"}
        except Exception as e:
            print(e)
            result = {"status": "error"}
        admin_user = User.objects.filter(is_superuser=True).first()
        all_users = User.objects.all().exclude(username=admin_user.username)
        list_user = []
        for usr in all_users:
            usr_serializer = UserBaseSerializer(usr)
            list_user.append(usr_serializer.data)
        result.update({"user_details": list_user})
        return Response(data=result, status=status.HTTP_200_OK)


class ActivateUser(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        request_data = request.data
        print(request_data)
        user_id = request_data['user_id']
        user = User.objects.filter(id=user_id).first()
        try:
            print(user)
            user.is_active = True
            user.save()
            result = {"status": "success"}
        except Exception as e:
            print(e)
            result = {"status": "error"}
        admin_user = User.objects.filter(is_superuser=True).first()
        all_users = User.objects.all().exclude(username=admin_user.username)
        list_user = []
        for usr in all_users:
            usr_serializer = UserBaseSerializer(usr)
            list_user.append(usr_serializer.data)
        result.update({"user_details": list_user})
        return Response(data=result, status=status.HTTP_200_OK)


class UpdateProfilePicture(generics.GenericAPIView):

    def put(self, request, *args, **kwargs):
        print(request.data)
        print(kwargs['pk'])
        validated_data = request.data
        user = User.objects.get(id=kwargs['pk'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.email = validated_data['email']
        user.username = validated_data['username']
        user.profile_image = request.FILES['profile_image']
        user.is_active = True
        user.save()
        return Response({
            'data': "User Profile Updated"
        },
            status=status.HTTP_200_OK,
        )
