from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


# Create your views here.

class CreateUserApiView(CreateAPIView):
    serializer_class = UserSerializer


class LogoutApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': 'logged out'})
