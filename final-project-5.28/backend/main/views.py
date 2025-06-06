from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Stock
from .serializers import StockSerializer


class StockSearchView(APIView):
    """주식 검색 API"""

    def get(self, request):
        query = request.query_params.get("query", None)
        if query:
            # 종목명 또는 종목코드로 검색 (대소문자 구분 없이)
            stocks = Stock.objects.filter(
                Q(stock_name__icontains=query) | Q(stock_code__icontains=query)
            )[
                :20
            ]  # 검색 결과는 최대 20개로 제한
            serializer = StockSerializer(stocks, many=True)
            return Response(serializer.data)
        return Response(
            {"message": "검색어를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST
        )
