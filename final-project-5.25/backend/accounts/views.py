from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login, logout
from .serializers import (
    SignUpSerializer, UserProfileSerializer, SurveySerializer,
    UserActivitySerializer, StockRecommendationSerializer, SavingRecommendationSerializer
)
from .models import UserActivity, StockRecommendation, SavingRecommendation
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from django.middleware.csrf import get_token
import random

User = get_user_model()


class CSRFTokenView(APIView):
    """CSRF 토큰 제공 API"""
    permission_classes = [AllowAny]
    
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({'csrfToken': get_token(request)})


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
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response(
                {"message": "사용자명과 비밀번호를 입력해주세요."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 로그인 활동 기록
            UserActivity.objects.create(
                user=user,
                activity_type='login',
                description=f'{user.username}님이 로그인했습니다.'
            )
            return Response(
                {"message": "로그인 성공", "username": user.username, "email": user.email}
            )
        return Response({"message": "로그인 실패"}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name="dispatch")
class LogOutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃 완료"})


class CurrentUserView(APIView):
    """현재 로그인된 사용자 정보 확인 API"""
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "username": request.user.username,
                "email": request.user.email,
                "is_authenticated": True
            })
        else:
            return Response({
                "is_authenticated": False
            }, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "프로필이 수정되었습니다."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(user)
        return Response(serializer.data)


class SurveyView(APIView):
    """설문조사 API"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        user = request.user
        serializer = SurveySerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            # 설문조사 완료 표시
            user.survey_completed = True
            user.survey_completed_date = timezone.now()
            serializer.save()
            
            # 설문조사 완료 활동 기록
            UserActivity.objects.create(
                user=user,
                activity_type='survey_completed',
                description='투자 성향 설문조사를 완료했습니다.'
            )
            
            # 설문조사 결과를 바탕으로 추천 생성
            self.generate_recommendations(user)
            
            return Response({
                "message": "설문조사가 완료되었습니다.",
                "survey_data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_recommendations(self, user):
        """설문조사 결과를 바탕으로 추천 생성"""
        # 주식 추천 생성
        self.generate_stock_recommendations(user)
        # 예적금 추천 생성
        self.generate_saving_recommendations(user)

    def generate_stock_recommendations(self, user):
        """주식 추천 생성 (간단한 로직)"""
        stock_recommendations = []
        
        if user.investment_style == 'conservative':
            # 안전형 - 대형주, 배당주 추천
            stocks = [
                {'code': '005930', 'name': '삼성전자', 'reason': '안정적인 대형주로 배당 수익 기대'},
                {'code': '000660', 'name': 'SK하이닉스', 'reason': '반도체 업계 선두주자로 안정성 높음'},
                {'code': '035420', 'name': 'NAVER', 'reason': '국내 IT 대표주로 꾸준한 성장세'}
            ]
        elif user.investment_style == 'moderate':
            # 중립형 - 성장주와 안정주 혼합
            stocks = [
                {'code': '005930', 'name': '삼성전자', 'reason': '안정성과 성장성을 겸비한 대형주'},
                {'code': '035720', 'name': '카카오', 'reason': '플랫폼 기업으로 성장 가능성 높음'},
                {'code': '207940', 'name': '삼성바이오로직스', 'reason': '바이오 산업의 성장주'}
            ]
        else:  # aggressive
            # 공격형 - 성장주, 테마주 추천
            stocks = [
                {'code': '035720', 'name': '카카오', 'reason': '디지털 전환 수혜주로 고성장 기대'},
                {'code': '373220', 'name': 'LG에너지솔루션', 'reason': '전기차 배터리 시장 선도'},
                {'code': '068270', 'name': '셀트리온', 'reason': '바이오시밀러 글로벌 진출 기대'}
            ]
        
        for stock in stocks:
            StockRecommendation.objects.create(
                user=user,
                stock_code=stock['code'],
                stock_name=stock['name'],
                recommendation_reason=stock['reason'],
                confidence_score=random.uniform(0.7, 0.9)
            )

    def generate_saving_recommendations(self, user):
        """예적금 추천 생성 (간단한 로직)"""
        saving_recommendations = []
        
        if user.monthly_investment_amount == 'under_50':
            # 소액 투자자 - 자유적금 추천
            products = [
                {'name': 'KB Star 자유적금', 'bank': 'KB국민은행', 'rate': 3.2, 'type': 'saving', 'reason': '소액으로도 시작 가능한 자유적금'},
                {'name': '신한 쏠편한 적금', 'bank': '신한은행', 'rate': 3.1, 'type': 'saving', 'reason': '유연한 납입 조건의 적금상품'}
            ]
        elif user.monthly_investment_amount in ['50_100', '100_300']:
            # 중간 투자자 - 정기적금 추천
            products = [
                {'name': '하나 청년도약적금', 'bank': '하나은행', 'rate': 4.5, 'type': 'saving', 'reason': '청년층 대상 고금리 적금'},
                {'name': 'NH 올원 정기예금', 'bank': 'NH농협은행', 'rate': 3.8, 'type': 'deposit', 'reason': '안정적인 정기예금 상품'}
            ]
        else:  # over_300
            # 고액 투자자 - 특판 상품 추천
            products = [
                {'name': '우리 WON 정기예금', 'bank': '우리은행', 'rate': 4.2, 'type': 'deposit', 'reason': '고액 예치 시 우대금리 적용'},
                {'name': 'IBK 기업 정기적금', 'bank': 'IBK기업은행', 'rate': 4.0, 'type': 'saving', 'reason': '목돈 마련을 위한 정기적금'}
            ]
        
        for product in products:
            SavingRecommendation.objects.create(
                user=user,
                product_name=product['name'],
                bank_name=product['bank'],
                interest_rate=product['rate'],
                product_type=product['type'],
                recommendation_reason=product['reason']
            )


class RecommendationView(APIView):
    """추천 결과 조회 API"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # 주식 추천
        stock_recommendations = StockRecommendation.objects.filter(user=user)[:5]
        stock_serializer = StockRecommendationSerializer(stock_recommendations, many=True)
        
        # 예적금 추천
        saving_recommendations = SavingRecommendation.objects.filter(user=user)[:5]
        saving_serializer = SavingRecommendationSerializer(saving_recommendations, many=True)
        
        return Response({
            'stock_recommendations': stock_serializer.data,
            'saving_recommendations': saving_serializer.data
        })


class UserActivityView(APIView):
    """사용자 활동 기록 API"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        activities = UserActivity.objects.filter(user=user)[:20]  # 최근 20개
        serializer = UserActivitySerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request):
        """활동 기록 추가"""
        user = request.user
        activity_type = request.data.get('activity_type')
        description = request.data.get('description')
        
        UserActivity.objects.create(
            user=user,
            activity_type=activity_type,
            description=description
        )
        
        return Response({"message": "활동이 기록되었습니다."})


class UserStocksView(APIView):
    """사용자 주식 관리 API"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """보유주식 또는 관심주식 추가"""
        user = request.user
        stock_type = request.data.get('type')  # 'owned' or 'interested'
        stock_data = request.data.get('stock_data')
        
        if stock_type == 'owned':
            if stock_data not in user.owned_stocks:
                user.owned_stocks.append(stock_data)
        elif stock_type == 'interested':
            if stock_data not in user.interested_stocks:
                user.interested_stocks.append(stock_data)
        
        user.save()
        
        # 활동 기록
        UserActivity.objects.create(
            user=user,
            activity_type='stock_search',
            description=f'{stock_data.get("name", "주식")}을(를) {"보유주식" if stock_type == "owned" else "관심주식"}에 추가했습니다.'
        )
        
        return Response({"message": "주식이 추가되었습니다."})

    def delete(self, request):
        """보유주식 또는 관심주식 제거"""
        user = request.user
        stock_type = request.data.get('type')
        stock_code = request.data.get('stock_code')
        
        if stock_type == 'owned':
            user.owned_stocks = [stock for stock in user.owned_stocks if stock.get('code') != stock_code]
        elif stock_type == 'interested':
            user.interested_stocks = [stock for stock in user.interested_stocks if stock.get('code') != stock_code]
        
        user.save()
        return Response({"message": "주식이 제거되었습니다."})


class UserYoutubeView(APIView):
    """사용자 유튜브 관리 API"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """나중에 볼 영상 또는 구독 채널 추가"""
        user = request.user
        content_type = request.data.get('type')  # 'video' or 'channel'
        content_data = request.data.get('content_data')
        
        if content_type == 'video':
            if content_data not in user.watch_later_videos:
                user.watch_later_videos.append(content_data)
        elif content_type == 'channel':
            if content_data not in user.subscribed_channels:
                user.subscribed_channels.append(content_data)
        
        user.save()
        
        # 활동 기록
        UserActivity.objects.create(
            user=user,
            activity_type='video_watch',
            description=f'{content_data.get("title", "컨텐츠")}을(를) {"나중에 볼 영상" if content_type == "video" else "구독 채널"}에 추가했습니다.'
        )
        
        return Response({"message": "컨텐츠가 추가되었습니다."})

    def delete(self, request):
        """나중에 볼 영상 또는 구독 채널 제거"""
        user = request.user
        content_type = request.data.get('type')
        content_id = request.data.get('content_id')
        
        if content_type == 'video':
            user.watch_later_videos = [video for video in user.watch_later_videos if video.get('video_id') != content_id]
        elif content_type == 'channel':
            user.subscribed_channels = [channel for channel in user.subscribed_channels if channel.get('channel_id') != content_id]
        
        user.save()
        return Response({"message": "컨텐츠가 제거되었습니다."})
