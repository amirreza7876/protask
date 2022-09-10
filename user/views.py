from django.db.utils import IntegrityError
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_serializer = UserSerializer(user, context=self.get_serializer_context())
        token = get_tokens_for_user(user)
        return Response({
            **token,
            "user": user_serializer.data,
        }, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    if request.method == 'GET':
        return Response({"username": request.user.username, 'email': request.user.email, 'bio': request.user.bio})

    if request.method == 'POST':
        print(request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        bio = request.data.get('bio')
        user = request.user
        try:
            if email:
                user.email = email
                user.save()
            if username:
                user.username = username
                user.save()
        except IntegrityError as error:
            return Response({'field error': error.args[0].split('.')[1]})

        if password:
            user.set_password(password)
            user.save()
        if bio:
            user.bio = bio
            user.save()
        return Response({'msg': 'updated'}, status=status.HTTP_202_ACCEPTED)
