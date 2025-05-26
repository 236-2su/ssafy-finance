from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_field


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        Saves a new user instance.
        Populates a user instance with data from the sociallogin.
        """
        user = sociallogin.user
        user.username = (
            user.username or sociallogin.account.uid
        )  # 기본 username이 없다면 uid 사용

        # 이메일 설정 (sociallogin.user.email이 우선)
        email = sociallogin.user.email
        if (
            not email and sociallogin.account.extra_data
        ):  # sociallogin.user.email이 없고 extra_data가 있을 때
            if sociallogin.provider == "kakao":
                kakao_account = sociallogin.account.extra_data.get("kakao_account")
                if kakao_account:
                    email = kakao_account.get("email")
            elif sociallogin.provider == "google":
                email = sociallogin.account.extra_data.get("email")

        if email:
            user_email(user, email)

        # 닉네임 설정
        nickname = None
        if sociallogin.provider == "google":
            nickname = sociallogin.account.extra_data.get("name")
        elif sociallogin.provider == "kakao":
            properties = sociallogin.account.extra_data.get("properties")
            if properties:
                nickname = properties.get("nickname")

        if nickname:
            user_field(user, "nickname", nickname)

        # 프로필 이미지 URL 설정
        profile_img_url = None
        if sociallogin.provider == "google":
            profile_img_url = sociallogin.account.extra_data.get("picture")
        elif sociallogin.provider == "kakao":
            properties = sociallogin.account.extra_data.get("properties")
            if properties:
                profile_img_url = properties.get("profile_image")

        if profile_img_url:
            user_field(user, "profile_img", profile_img_url)

        # 부모 클래스의 save_user 호출 전에 user 객체에 필요한 값을 채워넣고,
        # 그 다음에 부모 save_user를 호출하여 실제 저장을 위임하거나,
        # 여기서 직접 user.save()를 호출할 수 있습니다.
        # 여기서는 sociallogin.user 객체를 직접 수정했으므로,
        # 부모의 save_user를 호출하기보다는 여기서 저장하거나,
        # populate_user에서 처리하고 부모 save_user가 저장하도록 합니다.

        # 여기서는 populate_user에서 처리하도록 하고, save_user는 기본 동작을 따르도록 변경 시도
        # super().save_user를 호출하기 전에 user 객체를 sociallogin.user로 설정
        sociallogin.user = user
        # 실제 저장은 super().save_user()에 맡김
        # 하지만, 이미 위에서 user 객체를 가져와서 수정했으므로,
        # super().save_user()가 새 사용자를 만들지 않도록 주의해야 함.
        # DefaultSocialAccountAdapter의 save_user는 이미 존재하는 사용자인지 확인 후 처리함.

        # 명시적으로 저장
        user.save()
        return user

    def populate_user(self, request, sociallogin, data):
        """
        Populates user instance with data from social account.
        """
        user = super().populate_user(request, sociallogin, data)
        # 여기서 추가적인 사용자 정보(예: 닉네임, 프로필 이미지)를 설정할 수 있습니다.
        # save_user에서 처리하므로 여기서는 특별한 작업을 하지 않아도 됩니다.
        return user
