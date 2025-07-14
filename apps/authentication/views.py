import random
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User, OTP
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

def generate_otp():
    """Generate a random 6-digit OTP"""
    return str(random.randint(100000, 999999))

# /auth/signup
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)

# /auth/send-otp
class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            purpose = serializer.validated_data['purpose']
            otp_code = generate_otp()
            OTP.objects.create(mobile=mobile, code=otp_code, purpose=purpose)
            return Response({'otp': otp_code}, status=200)  # Return mock OTP
        return Response(serializer.errors, status=400)

# /auth/verify-otp
class VerifyOTPView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            otp = serializer.validated_data['otp']
            otp_obj = OTP.objects.filter(mobile=mobile, code=otp).order_by('-created_at').first()
            if otp_obj and otp_obj.is_valid():
                user, _ = User.objects.get_or_create(mobile=mobile)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Invalid or expired OTP'}, status=400)
        return Response(serializer.errors, status=400)

# /auth/forgot-password
class ForgotPasswordOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            if not User.objects.filter(mobile=mobile).exists():
                return Response({'error': 'User not found'}, status=404)
            otp_code = generate_otp()
            OTP.objects.create(mobile=mobile, code=otp_code, purpose='reset')
            return Response({'otp': otp_code}, status=200)
        return Response(serializer.errors, status=400)

# /auth/change-password
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Incorrect old password'}, status=400)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=400)

# /user/me
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
