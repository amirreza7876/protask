from rest_framework import generics, permissions, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    return Response({"username": request.user.username})

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

# class MyTokenVerifyView(TokenVerifyView):
#     serializer_class = MyTokenVerifySerializer
#     def get_serializer_context(self):
#         context = super(MyTokenVerifyView, self).get_serializer_context()
#         context.update({"request": self.request})
#         return context
