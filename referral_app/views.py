from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer
from .tasks import send_authcode
from .utils import *


@api_view(['POST'])
def authenticate_phoneAPIView(request):   # получения номера телефона, создание и отправка кода
    phone = request.data.get('phone')
    profile_queryset = Profile.object.filter(phone=phone)

    # TODO проверка валидности номера телефона при отправке

    if profile_queryset.exists():
        pass
        # profile = profile_queryset[0]
    else:
        Profile.object.create_profile(phone)

    if redis_auth_code.exists(phone) == 0:
        authcode = create_auth_code(phone)
        send_authcode.delay(phone, authcode)

    return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
def authenticate_codeAPIView(request):
    authcode = request.data.get('authcode')
    phone = request.data.get('phone')

    code_redis = redis_auth_code.get(phone)
    if code_redis:
        code_redis = code_redis.decode("utf-8")

        if code_redis == authcode:
            profile = Profile.object.get(phone=phone)

            token = get_tokens(profile.phone)
            return Response(ProfileSerializer(
                {'phone': profile.phone, 'invite_code': profile.invite_code, 'token': token['jwt'], 'token_refresh': token['refresh']}, ).data)

    return Response({'error': 'неверные данные',}, status=status.HTTP_400_BAD_REQUEST)


# TODO продумать и сделать рефреш токен-систему и дальнейший функционал


@api_view(['POST'])
def authenticate_refresh_tokenAPIView(request):
    token_refresh_elem = request.data.get('token_refresh')
    phone = request.data.get('phone')

    token_refresh_redis = redis_refresh_token.get(phone)

    redis_refresh_token.delete(phone)
    redis_auth_code.delete(phone)

    if token_refresh_redis:
        token_refresh_redis = token_refresh_redis.decode("utf-8")
        if token_refresh_elem == token_refresh_redis:
            token = get_tokens(phone)
            return Response({'token': token['jwt'], 'token_refresh': token['refresh']}, )

    return Response({'error': 'неверные данные', }, status=status.HTTP_400_BAD_REQUEST)


