import datetime

# client_id = 6b2e577ab7cea4063c1a
# client secret = 8e1b66ee4cf17e7574ceadf8d49e4cdfa3d99395
import logging

from django.db import transaction
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken

from core.models import User
from expectations.models import ManagingExpectation
from expectations.utils import check_credential
from expectations.serializers import UserCreateSerializer, GetExpectationSerializer, ExpectationSerializer, GithubAuthSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    __doc__ = "Registration API for user"

    def post(self, request, *args, **kwargs):
        logging.info("New User Registration data")
        logging.info(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.instance
            user.set_password(request.data["password"])
            user.save()
            payload = jwt_payload_handler(user)
            jwt_token = jwt_encode_handler(payload)
            response_data = {"token": jwt_token, 'data': serializer.data}
            response_status = status.HTTP_201_CREATED
        else:
            response_data = serializer.errors
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(response_data, status=response_status)


class LoginAPIView(ObtainJSONWebToken):
    __doc__ = "This api is used to login"

    def post(self, request, *args, **kwargs):
        if not "email" in request.data:
            return Response(
                {"email": "This Field is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(
            Q(email=request.data["email"]) | Q(username=request.data["email"])
        ).first()

        if not user:
            return Response({"user": "USER_NOT_EXIST"})
        user = check_credential(user=user, data=self.request.data)
        if user:
            payload = jwt_payload_handler(user)
            jwt_token = jwt_encode_handler(payload)
            user.last_login = datetime.datetime.now()
            user.save()
            return Response({'token': jwt_token})
        else:
            return Response({'errors': "Wrong Password"})


class GetExpectationListView(generics.ListAPIView):
    serializer_class = GetExpectationSerializer
    permission_classes = (IsAuthenticated, )
    __doc__ = "This api is used to get the list of all team members expectations role and finished time"

    def get_queryset(self):
        queryset = ManagingExpectation.objects.filter(is_archive=False).select_related('user')
        return queryset


class ManagingExpectations(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpectationSerializer
    permission_classes = (IsAuthenticated, )
    __doc__ = "This api is used to create, update and delete the team members expectations role and finished time"

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                instance = serializer.save(user=request.user)
                serializer = self.serializer_class(instance)
                response = serializer.data
                response_status = status.HTTP_201_CREATED
            else:
                response = serializer.errors
                response_status = status.HTTP_400_BAD_REQUEST
            return Response(response, status=response_status)

    def patch(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = get_object_or_404(ManagingExpectation, id=self.kwargs.get('pk'))
            if instance.user == request.user:
                serializer = self.serializer_class(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    serializer = self.serializer_class(instance)
                    response_data = serializer.data
                    response_status = status.HTTP_201_CREATED
                else:
                    response_data = serializer.errors
                    response_status = status.HTTP_400_BAD_REQUEST
            else:
                response_data = {'status': False}
                response_status = status.HTTP_401_UNAUTHORIZED
            return Response(response_data, status=response_status)

    def delete(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = get_object_or_404(ManagingExpectation, id=self.kwargs.get('pk'))
            if instance.user == request.user:
                self.perform_destroy(instance)
                response_data = {'status': True}
                response_status = status.HTTP_200_OK
            else:
                response_data = {'status': False}
                response_status = status.HTTP_401_UNAUTHORIZED
            return Response(response_data, status=response_status)


class GithubSignUpAuthView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = GithubAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response, response_status = serializer.check_auth(request)
        return Response(response, status=response_status)
