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
