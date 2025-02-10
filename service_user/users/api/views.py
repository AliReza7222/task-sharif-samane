from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User

from .serializers import UserCreateSerializer, UserRetrieveSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    lookup_field = "id"
