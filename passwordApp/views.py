# registration_app/views.py

from rest_framework import status,generics
# from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer,UserLoginSerializer,ChangePasswordSerializer,UserViewSeriializer,EditUserSerializer,OrganizationSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from knox.models import AuthToken
from .models import RegiUser,Organization
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny



#1. SignUp the user

class UserRegistration(generics.CreateAPIView):
    queryset = RegiUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

            # You can customize the response data as needed
            response_data = {
                "message": "User registered successfully",
                "user_id": user.id,
                "email": user.email,
                "token":token.key
            }
          
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


#2. Login User
class UserLogin(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request=request, email=email, password=password)

            if user is not None:
                response_data = {
                "message": "User Login successfully",
                "user_id": user.id,
                "email": user.email,
            }
          
                token, _ = Token.objects.get_or_create(user=user)
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


#3. Change the password of the user

class ChangePassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['old_password']


            user = authenticate(request=request, email=email, password=password)
            # Check if the old password matches
            if not user.check_password(serializer.validated_data['old_password']):
                
                return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password and save the user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            response_data = {
            "message": "Password updated successfully",
            "user_id": user.id,
            "email": user.email,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#4. Fetch the user details so user can view their details    
class ViewUserDetails(generics.RetrieveAPIView):
  
    def get(self, request):
        email = request.query_params.get('email')  
        if email:
            try:
                user = RegiUser.objects.get(email=email)  
                serializer = UserViewSeriializer(user)  
                response_data = {
                'message' :"User Details Fetched Successfully",
                'user_id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
                return Response(response_data)
            except User.DoesNotExist:
                return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Email parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        

#5. User can edit their details
class EditUserDetails(generics.UpdateAPIView):
    serializer_class = EditUserSerializer
    # permission_classes = [IsAuthenticated]
    # allowed_methods = ['PUT', 'PATCH']
    queryset = RegiUser.objects.all()

    def get_object(self):
        print("self.request:", self.request) 
        email = self.request.data.get('email', None)
        if email:
            return self.queryset.get(email=email)
        return self.request.user  
    
    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            print("Serializer data:", serializer.validated_data) 
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUES)
    
        self.perform_update(serializer)
        response ={
            "message":"User Details edited successfully",
            "data":serializer.data
            }
        return Response(response)
        
       
# 3. Create the organization
class CreateOrganization(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    
    







  