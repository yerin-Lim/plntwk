from .serializers import UserSerializer,CustomLoginSerializer,CustomRegisterSerializer
from .models import CustomerUser
from rest_framework import generics,permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_auth.views import LoginView, LogoutView
from rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import status
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token

class UserView(generics.ListCreateAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = UserSerializer

class CustomLogin(LoginView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomLoginSerializer

class CustomLogout(LogoutView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomLoginSerializer

class RegisterUserView(generics.ListCreateAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomRegisterSerializer

    def post(self, request):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request) # <---- INCLUDE REQUEST
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors ,status=status.HTTP_400_BAD_REQUEST)