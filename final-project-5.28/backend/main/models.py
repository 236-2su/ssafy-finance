from django.db import models


class Stock(models.Model):
    """주식 정보를 저장하는 모델"""

    stock_code = models.CharField(max_length=20, unique=True, verbose_name="종목코드")
    stock_name = models.CharField(max_length=100, verbose_name="종목명")
    # 필요하다면 시장 구분 (KOSPI, KOSDAQ 등) 필드 추가 가능
    # market_type = models.CharField(max_length=10, blank=True, null=True, verbose_name="시장구분")

    def __str__(self):
        return f"{self.stock_name} ({self.stock_code})"

    class Meta:
        verbose_name = "주식 정보"
        verbose_name_plural = "주식 정보 목록"
        ordering = ["stock_name"]
