# registration_app/urls.py

from django.urls import path
from .views import UserRegistration,UserLogin,ChangePassword,ViewUserDetails,EditUserDetails,CreateOrganization


urlpatterns = [
    # path('api/token/', CustomAuthToken.as_view(), name='token'),
    path('signUp', UserRegistration.as_view(), name='user-registration'),
    path('login', UserLogin.as_view(), name='user-login'),
    path('change_password', ChangePassword.as_view(), name='change-password'),
    path('view_user_details/', ViewUserDetails.as_view(), name='view_user_details'),
    path('edit_user_details/', EditUserDetails.as_view(), name='edit_user_details'),
    path('create_organization', CreateOrganization.as_view(), name='create_organization'),

]
