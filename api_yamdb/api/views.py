from random import choice
from string import ascii_lowercase, digits

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from .serializers import ConfirmationCodeSerializer, UserSerializer
from .permissions import IsAdmin

CONFIRMATION_CODE_CHARS = tuple(ascii_lowercase + digits)


class APIUser(APIView):
    """Класс для переопределения запросов GET и PATCH"""
    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(
            'Вы не авторизованы',
            status=status.HTTP_401_UNAUTHORIZED
        )

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST
                            )
        return Response('Вы не авторизованы',
                        status=status.HTTP_401_UNAUTHORIZED
                        )


class UserViewSet(viewsets.ModelViewSet):
    """Класс UserViewSet для User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]


@api_view(['POST'])
def send_mail(request):
    """Отправляет код подтверждения на e-mail."""
    serializer = ConfirmationCodeSerializer(data=request.data)
    email = request.data.get('email', False)
    if serializer.is_valid():
        cc_lst = []
        for number_of_symbols in range(16):
            cc_lst.append(choice(CONFIRMATION_CODE_CHARS))
        confirmation_code = ''.join(cc_lst)
        user = User.objects.filter(email=email).exists()
        if not user:
            User.objects.create_user(email=email)
        User.objects.filter(email=email).update(
            confirmation_code=make_password(
                confirmation_code, salt=None, hasher='default'
            )
        )
        mail_subject = 'Код подтверждения'
        message = confirmation_code
        send_mail(mail_subject, message, [email])
        return Response(f'Код отправлен на почту {email}',
                        status=status.HTTP_200_OK
                        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    """Получает JWT-токен"""
    serializer = ConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)
        if check_password(confirmation_code, user.confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Неверный код подтверждения'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
