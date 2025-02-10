from django.urls import path

from .views import UserCreateAPIView, UserRetrieveAPIView

app_name = "users_api"
urlpatterns = [
    path("users/create/", UserCreateAPIView.as_view(), name="user-create"),
    path(
        "users/<str:user_id>/",
        UserRetrieveAPIView.as_view(),
        name="get-user",
    ),
]
