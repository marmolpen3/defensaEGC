from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import GetUserView, LogoutView, RegisterView, ChangeStyleView, ModifyView, ChangeSexView, ChangeEmailView


urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('changestyle/', ChangeStyleView.as_view()),
    path('register/', RegisterView.as_view()),
    path('modify/', ModifyView.as_view(), name="register"),
    path('changesex/', ChangeSexView.as_view()),
    path('changeemail/', ChangeEmailView.as_view()),
]
