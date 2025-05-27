from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    home_address = models.CharField(
        max_length=255, blank=True, null=True
    )  # 집 주소 (선택)
    company_address = models.CharField(
        max_length=255, blank=True, null=True
    )  # 회사 주소 (선택)

    # 기타 선택 필드 (선택)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth = models.CharField(max_length=20, blank=True, null=True)
    customer_number = models.CharField(max_length=50, blank=True, null=True)

    # 설문조사 관련 필드
    stock_experience = models.CharField(
        max_length=20,
        choices=[
            ("none", "없음"),
            ("beginner", "초보 (1년 미만)"),
            ("intermediate", "중급 (1-3년)"),
            ("advanced", "고급 (3년 이상)"),
        ],
        blank=True,
        null=True,
    )
    investment_style = models.CharField(
        max_length=20,
        choices=[
            ("conservative", "안전형"),
            ("moderate", "중립형"),
            ("aggressive", "공격형"),
        ],
        blank=True,
        null=True,
    )
    monthly_investment_amount = models.CharField(
        max_length=20,
        choices=[
            ("under_50", "50만원 미만"),
            ("50_100", "50-100만원"),
            ("100_300", "100-300만원"),
            ("over_300", "300만원 이상"),
        ],
        blank=True,
        null=True,
    )
    investment_goal = models.CharField(
        max_length=30,
        choices=[
            ("short_term", "단기 수익"),
            ("long_term", "장기 투자"),
            ("retirement", "은퇴 준비"),
            ("emergency_fund", "비상 자금"),
        ],
        blank=True,
        null=True,
    )

    # 주식 관련 필드 (JSON으로 저장)
    owned_stocks = models.JSONField(default=list, blank=True)  # 보유주식 리스트
    interested_stocks = models.JSONField(default=list, blank=True)  # 관심주식 리스트

    # 유튜브 관련 필드
    watch_later_videos = models.JSONField(default=list, blank=True)  # 나중에 볼 영상
    subscribed_channels = models.JSONField(default=list, blank=True)  # 구독 채널

    # 설문조사 완료 여부
    survey_completed = models.BooleanField(default=False)
    survey_completed_date = models.DateTimeField(blank=True, null=True)


class UserActivity(models.Model):
    """사용자 활동 기록"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(
        max_length=20,
        choices=[
            ("login", "로그인"),
            ("news_view", "뉴스 조회"),
            ("video_watch", "영상 시청"),
            ("stock_search", "주식 검색"),
            ("saving_search", "예적금 검색"),
            ("community_post", "커뮤니티 글 작성"),
            ("community_comment", "댓글 작성"),
            ("survey_completed", "설문조사 완료"),
        ],
    )
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class StockRecommendation(models.Model):
    """주식 추천 결과"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stock_recommendations"
    )
    stock_code = models.CharField(max_length=20)
    stock_name = models.CharField(max_length=100)
    recommendation_reason = models.TextField()
    confidence_score = models.FloatField()  # 추천 신뢰도 (0-1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class SavingRecommendation(models.Model):
    """예적금 추천 결과"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="saving_recommendations"
    )
    product_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=50)
    interest_rate = models.FloatField()
    product_type = models.CharField(
        max_length=20, choices=[("deposit", "예금"), ("saving", "적금")]
    )
    recommendation_reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
