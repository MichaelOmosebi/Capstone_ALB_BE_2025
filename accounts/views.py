from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import CustomUser, Profile
from .serializers import RegisterSerializer, UserSerializer, ProfileSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        # Use the serializer to validate and save user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate token for the new user
        token, created = Token.objects.get_or_create(user=user)

        # Prepare custom response with token
        return Response({
            'user': serializer.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)



class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id, 'role': token.user.role})

class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile