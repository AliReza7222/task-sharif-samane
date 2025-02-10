from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from users.user import User

from .serializers import UserCreateSerializer, UserRetrieveSerializer


class UserCreateAPIView(GenericAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(user, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveAPIView(GenericAPIView):
    serializer_class = UserRetrieveSerializer

    def get(self, request, user_id):
        user = User.get_user_by_id(user_id)
        if not user:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(user)
        return Response(serializer.data)
