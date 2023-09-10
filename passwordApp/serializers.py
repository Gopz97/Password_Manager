from django.contrib.auth import get_user_model
from rest_framework import serializers
from passwordApp.models import RegiUser,Organization

User = get_user_model()  # Get the user model dynamically

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = RegiUser  # Use the User model obtained dynamically
        fields = ('email', 'password','first_name','last_name')  # Add other fields as needed

    def create(self, validated_data):
        # Create and return a new user with a hashed password
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)


class UserViewSeriializer(serializers.Serializer):
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegiUser
        fields = ('email', 'first_name', 'last_name')

    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def update(self, instance, validated_data):
            print("valdhh",validated_data)
            instance.email = validated_data.get('email', instance.email)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.save()
            return instance
    
    

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


