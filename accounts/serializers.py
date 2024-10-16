from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from xml.dom import ValidationErr
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from . utils import send_activation_email
from django.contrib.auth import get_user_model

User = get_user_model()
class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password', 'confirm_password']
        extra_kwargs={
        'password':{'write_only':True}
        }

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Password and Confirm-Password doesn't match!")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        user.is_active=False
        user.save()
        request=self.context.get('request') 
        send_activation_email(user,request)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number','email')



class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True,style={'input_type':'password'})
    class Meta:
        model=User
        # fields=('first_name', 'last_name', 'phone_number','email','password')
        fields=('email','password')
    def validate(self,data):
        email=data.get('email')
        password=data.get('password')
        if not email or not password:
            raise serializers.ValidationError("Email or password both are required")
        return data
    

class UserProfileSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(read_only=True)
    class Meta:
        model = User
        fields = ['email','first_name']
        read_only_fields=['email',]
        
    def update(self,instance,validated_data):
        instance.first_name=validated_data.get('first_name',instance.first_name)
        instance.save()
        return instance
    
    
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 50, style = {'input_type': 'password'}, write_only = True)
    confirm_password = serializers.CharField(max_length = 50, style = {'input_type':'password'}, write_only = True)
    
    class Meta:
        fields = ['password', 'confirm_password']
        
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        user = self.context.get('user')
        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm-Password doesn't match!")
        user.set_password(password)
        user.save()        
        return data 
        

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        fields = ['email']
    
    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('UserId', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost/3000/account/reset/'+uid+'/'+token
            print('Password Reset Link', link)
            
            # Send Email
            body = 'Click Following Link to Reset Your Password' +link
            data = {
                'subject' : 'Reset Your Password',
                'body' : body,
                'to_email' : user.email
            }
            # Util.send_email(data)
            return data 
        else:
            raise ValidationErr("You are not a registered user")
    

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 50, style = {'input_type': 'password'}, write_only = True)
    
    confirm_password = serializers.CharField(max_length = 50, style = {'input_type':'password'}, write_only = True)
    class Meta:
        fields = ['password', 'confirm_password']
        
    def validate(self, data):
        try:
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != confirm_password:
                raise serializers.ValidationError("Password and Confirm-Password doesn't match!")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()        
            return data 
        except DjangoUnicodeDecodeError:   # as identifier
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not Valid or Expired')