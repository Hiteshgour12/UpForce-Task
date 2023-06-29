from rest_framework import serializers,exceptions
from .models import *
from django.contrib import auth


class NewUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    #created_by = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['name','email', 'password','password2','mobile_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email']
        )
        name = self.validated_data['name']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        mobile_number = self.validated_data['mobile_number']


        if password != password2:
            raise serializers.ValidationError({"error": "Password doest not match"})
        user.set_password(password)
        user.name=name
        user.mobile_number=mobile_number
        user.is_active =True
        user.save()
        # Tenant_Registration.objects.create(signup_id=user)
        return user
    


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=68, write_only=True)
    tokens = serializers.SerializerMethodField()
    role = serializers.CharField(read_only=True)
    
    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens','role']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        # filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        # if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise exceptions.AuthenticationFailed('Invalid credentials, Try again')

        # if not user.status:
        #     raise exceptions.AuthenticationFailed('Email is not verified')


        return {
            'email': user.email,
            'tokens': user.tokens,
            'role':user.role
        }
    

class PostSerializer(serializers.ModelSerializer):
    liked_by = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all())
    class Meta:
        model = Post
        fields =['title','description','content','liked_by','status']
    def update(self, instance, validated_data):
        liked_by = validated_data.pop('liked_by')
        for i in liked_by:
            instance.liked_by.add(i)
        instance.save()
        return instance

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields ='__all__'

class LikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields =('liked_by', 'post','created_at')


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'