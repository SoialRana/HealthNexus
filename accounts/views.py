from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer,LoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer
from .serializers import RegistrationSerializer,LoginSerializer
from .models import User
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from .serializers import RegistrationSerializer
from django.contrib.sites.shortcuts import get_current_site

from rest_framework_simplejwt.tokens import RefreshToken
from . renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from .utils import send_activation_email
import logging
logger = logging.getLogger(__name__)
from django.core.mail import send_mail
import jwt
from django.conf import settings

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data,context={'request': request})

        if serializer.is_valid():
            user = serializer.save(request=request)
            send_activation_email(user,request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ActivationView(APIView):
    def get(self, request, token):
        try:
            # Decode the JWT token to get the user ID
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user_id = payload.get('user_id')

            # Get the user based on the ID
            user = User.objects.get(id=user_id)

            if user.is_active:
                return Response({'detail': 'Account already activated.'}, status=status.HTTP_200_OK)

            # Activate the user
            user.is_active = True
            user.save()
            return Response({'detail': 'Account activated successfully.'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'detail': 'Activation link has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApi(APIView):
    def post(self, request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(request, email=email, password=password)
            
            if user is None:
                return Response({
                    'status': 404,  # Unauthorized
                    'message': 'Your account is not activated. Please activate your account from the email',
                    'data': {}
                }, status=status.HTTP_404_NOT_FOUND)

            token=get_tokens_for_user(user)
            return Response({
                'msg' : 'login successful',
                'token': token,
                'user': LoginSerializer(user).data,
            }, status=status.HTTP_200_OK)
           
        return Response({
            'status': 400,
            'message': 'Validation error',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
            

from rest_framework.permissions import IsAuthenticated

class LogoutView(APIView):
    permission_classes=(IsAuthenticated,)
    # permission_classes=[IsAuthenticated]
    def post(self, request):
        # logout(request)
        refresh_token = request.data.get('refresh_token')
        print(type(refresh_token))
        if refresh_token:
            try:
                # Blacklist the refresh token
                token=RefreshToken(refresh_token)
                token.blacklist()
                return Response({'detail':'Successfully logged out'},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail':'Failed to logged out'+str(e)},status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'Refresh token is required'},status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self,request):
        user=request.user
        serializer=UserProfileSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Userdata Updated Successfully",
                            'data':serializer.data
                            }, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
class UserPasswordChangeView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format = None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid():
            return Response({'msg':'Password Change Successful'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, DecodeError

def generate_reset_token(user):
    payload={
        'user_id':user.id,
        'exp':datetime.utcnow()+timedelta(hours=1),
        'iat':datetime.utcnow(),
    }
    token=jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256')
    return token


class PasswordResetConfirmView(APIView):
    def post(self,request,token):
        try:
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
            user_id=payload.get('user_id')
        except ExpiredSignatureError:
            return Response({'detail': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user=User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail':'user does not exist'},status=status.HTTP_400_BAD_REQUEST)
        
        # validate new password
        new_password=request.data.get('new_password')
        if not new_password:
            return Response({'detail':'new password is required'},status=status.HTTP_400_BAD_REQUEST)
        
        # update the user's password
        user.set_password(new_password)
        user.save()
        return Response({'detail':'password has been reset successfully.'},status=status.HTTP_200_OK)

class PasswordResetEmailView(APIView):
    def post(self,request):
        email=request.data.get('email')
        if email is None:
            return Response({'detail': 'Email is required'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail':'User with this email does not exist.'},status=status.HTTP_400_BAD_REQUEST)
        
        # generate JWT token for password reset
        token=generate_reset_token(user)
        current_site=get_current_site(request)
        
        # create reset password link
        reset_link=f'http://{current_site.domain}/account/reset_password/{token}/'
        
        # send the email with the reset link
        send_mail(
            subject='Password Reset',
            message=f'Click the link below to reset your password:\n{reset_link}',
            from_email='zinanmuntasir123@gmail.com',
            recipient_list=[user.email],
        )
        return Response({'detail': 'password reset email sent.'},status=status.HTTP_200_OK)