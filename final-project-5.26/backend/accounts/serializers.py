from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserActivity, StockRecommendation, SavingRecommendation

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "home_address",
            "company_address",  # ✅ 추가 필드
        )

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            home_address=validated_data.get("home_address", ""),
            company_address=validated_data.get("company_address", ""),
        )


class UserProfileSerializer(serializers.ModelSerializer):
    """사용자 프로필 정보 시리얼라이저"""
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "home_address",
            "company_address",
            "phone",
            "birth",
            "customer_number",
            "stock_experience",
            "investment_style",
            "monthly_investment_amount",
            "investment_goal",
            "owned_stocks",
            "interested_stocks",
            "watch_later_videos",
            "subscribed_channels",
            "survey_completed",
            "survey_completed_date",
        )
        read_only_fields = ("id", "username")


class SurveySerializer(serializers.ModelSerializer):
    """설문조사 데이터 시리얼라이저"""
    class Meta:
        model = User
        fields = (
            "stock_experience",
            "investment_style",
            "monthly_investment_amount",
            "investment_goal",
            "owned_stocks",
            "interested_stocks",
        )


class UserActivitySerializer(serializers.ModelSerializer):
    """사용자 활동 기록 시리얼라이저"""
    class Meta:
        model = UserActivity
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at")


class StockRecommendationSerializer(serializers.ModelSerializer):
    """주식 추천 시리얼라이저"""
    class Meta:
        model = StockRecommendation
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at")


class SavingRecommendationSerializer(serializers.ModelSerializer):
    """예적금 추천 시리얼라이저"""
    class Meta:
        model = SavingRecommendation
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at")
