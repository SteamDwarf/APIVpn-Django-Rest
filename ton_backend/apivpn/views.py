from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, RegisterView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from apivpn.models import Todo
from apivpn.serializers import TodoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from dj_rest_auth.jwt_auth import set_jwt_cookies


class CustomOAuth2Client(OAuth2Client):
    def __init__(
        self,
        request,
        consumer_key,
        consumer_secret,
        access_token_method,
        access_token_url,
        callback_url,
        _scope,  # This is fix for incompatibility between django-allauth==65.3.1 and dj-rest-auth==7.0.1
        scope_delimiter=" ",
        headers=None,
        basic_auth=False,
    ):
        super().__init__(
            request,
            consumer_key,
            consumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            scope_delimiter,
            headers,
            basic_auth,
        )

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'todos': reverse('todos-list', request=request, format=format),
        'registration': reverse('registration', request=request, format=format)
    })


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/api/v1/auth/google/callback/"
    client_class = CustomOAuth2Client

    def post(self, request, *args, **kwargs):
        print(request)
        return super().post(request, *args, **kwargs)

class TodoView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class CustomRegisterViews(RegisterView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Если в ответе есть токены — перенесём их в cookie
        if "access" in response.data and "refresh" in response.data:
            set_jwt_cookies(
                response,
                access_token=response.data["access"],
                refresh_token=response.data["refresh"]
            )
            # (опционально) убрать из тела ответа
            del response.data["access"]
            del response.data["refresh"]

        return response