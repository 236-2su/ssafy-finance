from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login, logout
from .serializers import SignUpSerializer
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

User = get_user_model()


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "회원가입 성공"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogInView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(
                {"message": "로그인 성공", "username": user.username}  # ✅ 여기 추가
            )
        return Response({"message": "로그인 실패"}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name="dispatch")
class LogOutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃 완료"})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "username": user.username,
                "email": user.email,
                "home_address": user.home_address,
                "company_address": user.company_address,
            }
        )

    def put(self, request):
        user = request.user

        # 이메일, 주소 업데이트
        user.email = request.data.get("email", user.email)
        user.home_address = request.data.get("home_address", user.home_address)
        user.company_address = request.data.get("company_address", user.company_address)

        # 비밀번호 변경 처리
        new_password = request.data.get("new_password")
        password_confirm = request.data.get("password_confirm")

        if new_password or password_confirm:
            if new_password != password_confirm:
                return Response(
                    {"message": "비밀번호가 일치하지 않습니다."}, status=400
                )
            user.set_password(new_password)  # 비밀번호 암호화 저장

        user.save()
        return Response({"message": "프로필이 수정되었습니다."})


class ProfileDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "username": user.username,
                "email": user.email,
                "home_address": getattr(user, "home_address", ""),
                "company_address": getattr(user, "company_address", ""),
            }
        )
