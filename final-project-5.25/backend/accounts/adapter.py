from allauth.account.utils import user_email, user_field, user_username
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.contrib import messages

User = get_user_model()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        Saves a new user instance or connects an existing one.
        Populates a user instance with data from the sociallogin.
        """
        user = sociallogin.user  # This is a pre-filled User instance by allauth

        # 이메일 추출 로직 (기존 코드 활용)
        email = (
            sociallogin.user.email
        )  # allauth가 sociallogin.user에 이메일을 채워넣으려고 시도
        if (
            not email and sociallogin.account.extra_data
        ):  # sociallogin.user.email이 없을 때만 extra_data 확인
            if (
                sociallogin.account.provider == "kakao"
            ):  # 수정: sociallogin.provider -> sociallogin.account.provider
                kakao_account = sociallogin.account.extra_data.get("kakao_account")
                if kakao_account:
                    email = kakao_account.get("email")
            elif (
                sociallogin.account.provider == "google"
            ):  # 수정: sociallogin.provider -> sociallogin.account.provider
                email = sociallogin.account.extra_data.get("email")

        if not email:
            # 이메일이 없는 경우, 회원가입/로그인 처리를 중단하고 메시지 표시
            messages.error(
                request,
                "소셜 계정에서 이메일 정보를 가져올 수 없습니다. 다른 방법으로 로그인하거나, 소셜 계정의 이메일 설정을 확인해주세요.",
            )
            # 'account_login'은 allauth의 기본 로그인 URL 이름입니다. 프로젝트에 따라 다를 수 있습니다.
            # settings.LOGIN_URL을 사용하거나, urls.py에 정의된 이름을 사용해야 합니다.
            # 일반적으로 'account_login'이 맞습니다.
            raise ImmediateHttpResponse(redirect("account_login"))

        # 데이터베이스에서 이메일로 사용자 검색
        try:
            existing_user = User.objects.get(email=email)
            # 이메일이 존재하는 경우: 기존 사용자와 소셜 계정 연결 (로그인 처리)

            sociallogin.user = (
                existing_user  # sociallogin 객체의 user를 기존 사용자로 설정
            )

            # 소셜 계정을 기존 사용자와 연결합니다.
            # connect는 이미 연결된 경우 중복으로 처리하지 않습니다.
            # 또한, 이 과정에서 SocialAccount 객체가 생성/업데이트 됩니다.
            sociallogin.connect(request, existing_user)

            # 기존 사용자의 정보 업데이트 (선택 사항: 닉네임, 프로필 이미지 등)
            # 여기서는 소셜 프로필의 정보로 기존 정보를 덮어쓰지 않고, 비어있을 경우에만 채우도록 합니다.
            nickname = None
            if (
                sociallogin.account.provider == "google"
            ):  # 수정: sociallogin.provider -> sociallogin.account.provider
                nickname = sociallogin.account.extra_data.get("name")
            elif (
                sociallogin.account.provider == "kakao"
            ):  # 수정: sociallogin.provider -> sociallogin.account.provider
                properties = sociallogin.account.extra_data.get("properties")
                if properties:
                    nickname = properties.get("nickname")

            if nickname and not existing_user.nickname:
                user_field(existing_user, "nickname", nickname)

            profile_img_url = None
            if (
                sociallogin.account.provider == "google"
            ):  # 수정: sociallogin.provider -> sociallogin.account.provider
                profile_img_url = sociallogin.account.extra_data.get("picture")
            elif (
                sociallogin.account.provider == "kakao"
            ):  # 수정: sociallogin.provider -> sociallogin.account.provider
                properties = sociallogin.account.extra_data.get("properties")
                if properties:
                    profile_img_url = properties.get("profile_image")

            if profile_img_url and not existing_user.profile_img:
                user_field(existing_user, "profile_img", profile_img_url)

            existing_user.save()
            return existing_user

        except User.DoesNotExist:
            # 이메일이 존재하지 않는 경우: 신규 사용자 생성 (회원가입 처리)
            # sociallogin.user는 allauth에 의해 기본적인 User 인스턴스로 채워져 있습니다.
            # 이 user 객체에 추가 정보를 채워 저장합니다.

            # 사용자 이름 설정 (allauth가 이미 시도했을 수 있음, 없으면 uid 사용)
            # user_username 함수는 username을 설정하고 중복을 피하기 위한 로직을 포함할 수 있습니다.
            # 여기서는 sociallogin.user.username이 이미 채워져 있거나, 비어있다면 uid를 사용하도록 합니다.
            if not user.username:  # username이 비어있는 경우
                user_username(
                    user, sociallogin.account.uid
                )  # uid를 기본 username으로 사용

            # 이메일 설정 (위에서 추출한 email 사용)
            user_email(
                user, email
            )  # user_email은 user.email = email과 유사하나, 추가 처리가 있을 수 있음

            # 닉네임 설정
            nickname = None
            if (
                sociallogin.account.provider == "google"
            ):  # 수정: sociallogin.provider -> sociallogin.account.provider
                nickname = sociallogin.account.extra_data.get("name")
            elif (
                sociallogin.account.provider == "kakao"
            ):  # 수정: sociallogin.provider -> sociallogin.account.provider
                properties = sociallogin.account.extra_data.get("properties")
                if properties:
                    nickname = properties.get("nickname")

            if nickname:
                user_field(user, "nickname", nickname)
            else:  # 닉네임이 없는 경우 이메일 앞부분을 기본값으로 사용
                user_field(user, "nickname", email.split("@")[0])

            # 프로필 이미지 URL 설정
            profile_img_url = None
            if (
                sociallogin.account.provider == "google"
            ):  # 수정: sociallogin.provider -> sociallogin.account.provider
                profile_img_url = sociallogin.account.extra_data.get("picture")
            elif (
                sociallogin.account.provider == "kakao"
            ):  # 수정: sociallogin.provider -> sociallogin.account.provider
                properties = sociallogin.account.extra_data.get("properties")
                if properties:
                    profile_img_url = properties.get("profile_image")

            if profile_img_url:
                user_field(user, "profile_img", profile_img_url)

            # user.save()를 호출하기 전에 sociallogin.save()를 호출하여
            # SocialAccount 레코드를 먼저 생성하고 user와 연결할 수 있습니다.
            # 그러나 DefaultSocialAccountAdapter의 save_user는 user.save() 이후에
            # sociallogin.save(request, connect=True)를 내부적으로 호출할 수 있습니다.
            # 여기서는 명시적으로 user를 저장하고, sociallogin.save()는
            # allauth의 흐름에 맡기거나, 필요시 명시적으로 호출합니다.
            # 지금 구조에서는 user를 저장하면 sociallogin이 이미 user와 연결되어 있으므로
            # 추가적인 sociallogin.save() 호출은 필요 없을 수 있습니다.
            # allauth는 sociallogin 객체를 통해 user와 social account를 연결하고 저장합니다.

            user.save()  # 새 사용자 저장
            sociallogin.save(request)  # social account 정보 저장 및 연결

            return user

    def populate_user(self, request, sociallogin, data):
        """
        Populates user instance with data from social account.
        This method is called before save_user for new users.
        """
        user = sociallogin.user  # Get the pre-filled user instance

        # 기본 username, email 등은 allauth가 어느정도 채워줍니다.
        # 여기서 추가적인 기본값 설정이나, sociallogin.account.extra_data를 사용한
        # 더 상세한 정보 채우기를 할 수 있습니다.
        # save_user에서 대부분의 로직을 처리하므로, 여기서는 최소한의 설정만 하거나 비워둘 수 있습니다.

        # 예시: username을 여기서 명시적으로 설정 (save_user에서도 처리 가능)
        # username = data.get('username', sociallogin.account.uid) # extra_data에서 username 가져오거나 uid 사용
        # user_username(user, username)

        # email은 save_user에서 더 정확하게 처리하므로 여기서는 건드리지 않거나,
        # data에서 가져온 값을 기본으로 설정할 수 있습니다.
        # email = data.get('email')
        # if email:
        # user_email(user, email)

        return super().populate_user(request, sociallogin, data)
