from rest_framework import serializers
from account.models import *
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util
from profileapi.models import *
from django.conf import settings 
from django.core.mail import send_mail

class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name', 'password','phoneNumber', 'password2', 'tc']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs
import requests

# url = "https://hourmailer.p.rapidapi.com/send"
url = "https://mail-sender-api1.p.rapidapi.com/"
# url =  "https://demo-project67614.p.rapidapi.com/catalog/product"


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')

        # Check if user exists
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID:', uid)

            # Generate password reset token
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token:', token)

            # Create the reset password link
<<<<<<< HEAD
            base_url = '127.0.0.1:8000' if settings.DEBUG else 'https://holanine.icu'
=======
            base_url = '127.0.0.1:8000' if settings.DEBUG else 'https://demoadmin.hola9.com'
>>>>>>> 8a72e49cd22e840587db7c1423cb1ca18330101d
            link = f'{base_url}/api/user/reset-password/{uid}/{token}'

            # Construct the email content
            subject = 'Reset Your Password'
            body = f'Click the following link to reset your password: {link}'

            # Send email using Django's send_mail
            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,  # Set your 'from' email address
                    recipient_list=[email],
                    fail_silently=False
                )
                print('Password reset email sent successfully!')
            except Exception as e:
                print(f'Error sending email: {e}')
                raise serializers.ValidationError('Failed to send password reset email.')

            return attrs
        else:
            raise serializers.ValidationError('You are not a registered user.')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')


class jobsRequiredSerialize(serializers.ModelSerializer):
  class Meta:
    model= JobsRequired
    fields= '__all__'


class jobdetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = JobApply
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True},
            'phone': {'required': True},
            'email': {'required': True},
            'title': {'required': True}
        }

    def validate(self, data):
        """
        Check that all fields are provided and not empty.
        """
        for field in data:
            if not data[field]:
                raise serializers.ValidationError(f"{field} field is required.")
        return data

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'
        
        
        
from rest_framework import serializers
from .models import Contact

class ContactEnquireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        
        
# from rest_framework import serializers
# from .models import EmployeeLogin

# class EmployeeLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmployeeLogin
#         fields = ['username', 'password']

class EmployeeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDetails
        fields = '__all__'
        
        
from .models import ReviewSection

class ReviewSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewSection
        fields = '__all__'


class LoginProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields =['id','name','phoneNumber']
      
      
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
