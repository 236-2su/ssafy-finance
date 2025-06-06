from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login, logout
from .serializers import (
    SignUpSerializer,
    UserProfileSerializer,
    SurveySerializer,
    UserActivitySerializer,
    StockRecommendationSerializer,
    SavingRecommendationSerializer,
)

# community 앱의 PostSerializer import
from community.serializers import PostSerializer
from community.models import Bookmark  # Bookmark 모델 import
from .models import (
    UserActivity,
    StockRecommendation,
    SavingRecommendation,
)  # User 모델은 get_user_model()로 가져옴
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.authentication import (
    SessionAuthentication,
)  # CSRF 보호와 함께 사용될 수 있음
from django.middleware.csrf import get_token
import random

User = get_user_model()


class CSRFTokenView(APIView):
    """CSRF 토큰 제공 API"""

    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({"csrfToken": get_token(request)})


class SignUpView(APIView):
    permission_classes = [AllowAny]  # 회원가입은 인증 없이 접근 가능해야 함

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
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            UserActivity.objects.create(
                user=user,
                activity_type="login",
                description=f"{user.username}님이 로그인했습니다.",
            )
            # UserProfileSerializer를 사용하여 사용자 정보 반환 (interested_stocks 포함되도록)
            serializer = UserProfileSerializer(user)
            return Response(
                {
                    "message": "로그인 성공",
                    "user": serializer.data,  # 사용자 전체 정보 반환
                }
            )
        return Response({"message": "로그인 실패"}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(
    csrf_exempt, name="dispatch"
)  # CSRF 보호 예외 처리 (필요에 따라 조정)
class LogOutView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인 된 사용자만 로그아웃 가능

    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃 완료"})


class CurrentUserView(APIView):
    permission_classes = [AllowAny]  # 또는 IsAuthenticated - 앱 로드 시 세션 확인용

    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserProfileSerializer(request.user)  # 전체 프로필 정보 반환
            return Response(
                {
                    "user": serializer.data,
                    "is_authenticated": True,
                }
            )
        else:
            return Response(
                {"is_authenticated": False}, status=status.HTTP_401_UNAUTHORIZED
            )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        # UserProfileSerializer가 interested_stocks를 read_only=False로 처리하거나,
        # 별도의 필드 업데이트 로직이 필요할 수 있음. 여기서는 UserProfileSerializer가 처리한다고 가정.
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "프로필이 수정되었습니다.", "user": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(APIView):
    permission_classes = [AllowAny]  # 다른 사용자 프로필은 누구나 볼 수 있도록

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)


class SurveyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = SurveySerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user.survey_completed = True
            user.survey_completed_date = timezone.now()
            serializer.save()  # user 객체에 변경사항 저장
            UserActivity.objects.create(
                user=user,
                activity_type="survey_completed",
                description="투자 성향 설문조사를 완료했습니다.",
            )
            # self.generate_recommendations(user) # 추천 생성 로직은 필요시 호출
            return Response(
                {
                    "message": "설문조사가 완료되었습니다.",
                    "survey_data": serializer.data,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # generate_recommendations, generate_stock_recommendations, generate_saving_recommendations 메서드는
    # ai_recommendations 앱으로 옮겨졌거나 별도 관리될 수 있으므로 여기서는 주석 처리 또는 삭제 검토


class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        stock_recommendations = StockRecommendation.objects.filter(user=user)[:5]
        stock_serializer = StockRecommendationSerializer(
            stock_recommendations, many=True
        )
        saving_recommendations = SavingRecommendation.objects.filter(user=user)[:5]
        saving_serializer = SavingRecommendationSerializer(
            saving_recommendations, many=True
        )
        return Response(
            {
                "stock_recommendations": stock_serializer.data,
                "saving_recommendations": saving_serializer.data,
            }
        )


class UserActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        activities = UserActivity.objects.filter(user=user).order_by("-created_at")[:20]
        serializer = UserActivitySerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request):  # 이 POST는 보통 특정 활동 발생 시 내부적으로 호출됨
        user = request.user
        activity_type = request.data.get("activity_type")
        description = request.data.get("description")
        if activity_type and description:
            UserActivity.objects.create(
                user=user, activity_type=activity_type, description=description
            )
            return Response(
                {"message": "활동이 기록되었습니다."}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": "activity_type과 description이 필요합니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserStocksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "owned_stocks": (
                    user.owned_stocks if isinstance(user.owned_stocks, list) else []
                ),
                "interested_stocks": (
                    user.interested_stocks
                    if isinstance(user.interested_stocks, list)
                    else []
                ),
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        user = request.user
        stock_type = request.data.get("type", "interested")
        stock_name = request.data.get("stock_name")
        stock_data = request.data.get("stock_data")

        if stock_type == "interested":
            if not stock_name:
                return Response(
                    {"error": "관심 주식 추가 시 stock_name이 필요합니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not isinstance(user.interested_stocks, list):
                user.interested_stocks = []
            if stock_name not in user.interested_stocks:
                user.interested_stocks.append(stock_name)
                user.save(update_fields=["interested_stocks"])
                UserActivity.objects.create(
                    user=user,
                    activity_type="interest_stock_add",
                    description=f"{stock_name}을(를) 관심주식에 추가했습니다.",
                )
                return Response(
                    {
                        "message": f"'{stock_name}'이(가) 관심 주식에 추가되었습니다.",
                        "interested_stocks": user.interested_stocks,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": f"'{stock_name}'은(는) 이미 관심 목록에 있습니다.",
                        "interested_stocks": user.interested_stocks,
                    },
                    status=status.HTTP_200_OK,
                )

        elif stock_type == "owned":
            if (
                not stock_data
                or not isinstance(stock_data, dict)
                or not stock_data.get("code")
                or not stock_data.get("name")
            ):
                return Response(
                    {
                        "error": "보유 주식 추가 시 유효한 stock_data (code, name 포함)가 필요합니다."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not isinstance(user.owned_stocks, list):
                user.owned_stocks = []

            if not any(s.get("code") == stock_data["code"] for s in user.owned_stocks):
                user.owned_stocks.append(stock_data)
                user.save(update_fields=["owned_stocks"])
                UserActivity.objects.create(
                    user=user,
                    activity_type="owned_stock_add",
                    description=f"{stock_data['name']}을(를) 보유주식에 추가했습니다.",
                )
                return Response(
                    {
                        "message": f"'{stock_data['name']}'이(가) 보유 주식에 추가되었습니다.",
                        "owned_stocks": user.owned_stocks,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": f"'{stock_data['name']}'은(는) 이미 보유 목록에 있습니다.",
                        "owned_stocks": user.owned_stocks,
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {
                    "error": "잘못된 stock_type입니다. 'interested' 또는 'owned'를 사용하세요."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request):
        user = request.user
        stock_type = request.data.get("type", "interested")
        stock_name = request.data.get("stock_name")
        stock_code = request.data.get("stock_code")

        if stock_type == "interested":
            if not stock_name:
                return Response(
                    {"error": "관심 주식 제거 시 stock_name이 필요합니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if (
                isinstance(user.interested_stocks, list)
                and stock_name in user.interested_stocks
            ):
                user.interested_stocks.remove(stock_name)
                user.save(update_fields=["interested_stocks"])
                UserActivity.objects.create(
                    user=user,
                    activity_type="interest_stock_remove",
                    description=f"{stock_name}을(를) 관심주식에서 제거했습니다.",
                )
                return Response(
                    {
                        "message": f"'{stock_name}'이(가) 관심 주식에서 제거되었습니다.",
                        "interested_stocks": user.interested_stocks,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": f"'{stock_name}'을(를) 관심 목록에서 찾을 수 없습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        elif stock_type == "owned":
            if not stock_code:
                return Response(
                    {"error": "보유 주식 제거 시 stock_code가 필요합니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not isinstance(user.owned_stocks, list):
                return Response(
                    {"error": "보유 주식 목록이 비어있거나 유효하지 않습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            original_len = len(user.owned_stocks)
            # 보유 주식은 객체 리스트이므로, code를 기준으로 필터링
            user.owned_stocks = [
                s for s in user.owned_stocks if s.get("code") != stock_code
            ]

            if len(user.owned_stocks) < original_len:
                user.save(update_fields=["owned_stocks"])
                # 활동 기록 시 제거된 주식의 이름을 찾으려고 시도할 수 있으나, 여기서는 코드로 기록
                UserActivity.objects.create(
                    user=user,
                    activity_type="owned_stock_remove",
                    description=f"주식(코드: {stock_code})을(를) 보유주식에서 제거했습니다.",
                )
                return Response(
                    {
                        "message": f"주식(코드: {stock_code})이(가) 보유 목록에서 제거되었습니다.",
                        "owned_stocks": user.owned_stocks,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "error": f"주식(코드: {stock_code})을(를) 보유 목록에서 찾을 수 없습니다."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": "잘못된 stock_type입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserYoutubeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        content_type = request.data.get("type")
        content_data = request.data.get("content_data")
        if content_type == "video":
            if not isinstance(user.watch_later_videos, list):
                user.watch_later_videos = []
            if not any(
                v.get("video_id") == content_data.get("video_id")
                for v in user.watch_later_videos
            ):
                user.watch_later_videos.append(content_data)
        elif content_type == "channel":
            if not isinstance(user.subscribed_channels, list):
                user.subscribed_channels = []
            if not any(
                c.get("channel_id") == content_data.get("channel_id")
                for c in user.subscribed_channels
            ):
                user.subscribed_channels.append(content_data)
        else:
            return Response(
                {"error": "잘못된 content_type입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.save()
        UserActivity.objects.create(
            user=user,
            activity_type="video_watch",
            description=f'{content_data.get("title", "컨텐츠")}을(를) {"나중에 볼 영상" if content_type == "video" else "구독 채널"}에 추가했습니다.',
        )
        return Response({"message": "컨텐츠가 추가되었습니다."})

    def delete(self, request):
        user = request.user
        content_type = request.data.get("type")
        content_id = request.data.get("content_id")  # video_id 또는 channel_id
        if content_type == "video":
            if not isinstance(user.watch_later_videos, list):
                user.watch_later_videos = []
            user.watch_later_videos = [
                v for v in user.watch_later_videos if v.get("video_id") != content_id
            ]
        elif content_type == "channel":
            if not isinstance(user.subscribed_channels, list):
                user.subscribed_channels = []
            user.subscribed_channels = [
                c for c in user.subscribed_channels if c.get("channel_id") != content_id
            ]
        else:
            return Response(
                {"error": "잘못된 content_type입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.save()
        return Response({"message": "컨텐츠가 제거되었습니다."})


class UserScrappedPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        bookmarks = (
            Bookmark.objects.filter(user=user)
            .select_related("post")
            .order_by("-created_at")
        )
        limit_str = request.query_params.get("limit", None)
        if limit_str:
            try:
                limit = int(limit_str)
                bookmarks = bookmarks[:limit]
            except ValueError:
                pass
        scrapped_posts = [
            bookmark.post for bookmark in bookmarks if bookmark.post is not None
        ]  # post가 null인 경우 제외
        serializer = PostSerializer(
            scrapped_posts, many=True, context={"request": request}
        )
        return Response(serializer.data)
