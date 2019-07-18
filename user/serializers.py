from rest_framework.serializers import ModelSerializer, Serializer
from .models import CustomerUser
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from allauth.account.adapter import get_adapter
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists, get_username_max_length)
from allauth.account.utils import setup_user_email

class CustomLoginSerializer(ModelSerializer,LoginSerializer):
    class Meta:
        model = CustomerUser
        fields = ['username','password']

class CustomRegisterSerializer(ModelSerializer,RegisterSerializer):
    class Meta:
        model = CustomerUser
        fields = ['email','username','password1','password2','name','nickname','gender','birth_date']

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    ("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(("The two password fields didn't match."))
        return data

    def validate_name(self,name):
        return name

    def validate_nickname(self,nickname):
        if CustomerUser.objects.filter(nickname=nickname).exists():
            raise  serializers.ValidationError(("이미 존재하는 닉네임입니다."))
        return nickname
    
    def validate_gender(self,gender):
        return gender
    
    def validate_birth_date(self,birth_date):
        return birth_date

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'gender': self.validated_data.get('gender', ''),
            'birth_date': self.validated_data.get('birth_date', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        user.nickname=self.cleaned_data['nickname']
        user.name=self.cleaned_data['name']
        user.gender=self.cleaned_data['gender']
        user.birth_date=self.cleaned_data['birth_date']

        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['email','username','name','nickname','gender','birth_date']