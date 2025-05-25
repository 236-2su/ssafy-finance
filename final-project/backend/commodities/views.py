import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import pandas as pd


@require_GET
def price_data(request):
    """
    GET parameters:
      - asset: 'gold' 또는 'silver'
      - start_date: 'YYYY-MM-DD' (선택)
      - end_date: 'YYYY-MM-DD' (선택)
    """
    asset = request.GET.get("asset")
    start = request.GET.get("start_date")
    end = request.GET.get("end_date")

    file_map = {
        "gold": "Gold_prices.xlsx",
        "silver": "Silver_prices.xlsx",
    }
    if asset not in file_map:
        return JsonResponse({"error": "Invalid asset"}, status=400)

    # BASE_DIR이 이미 backend 폴더를 가리키므로 commodities 폴더만 추가
    file_path = os.path.join(settings.BASE_DIR, "commodities", file_map[asset])
    print("📂 Loading Excel from:", file_path)

    try:
        df = pd.read_excel(file_path, parse_dates=["Date"])
        df = df.sort_values("Date")

        if start:
            df = df[df["Date"] >= pd.to_datetime(start)]
        if end:
            df = df[df["Date"] <= pd.to_datetime(end)]

        data = []
        for d, raw_price in zip(df["Date"], df["Close/Last"]):
            # 1) 원본이 '1,967.10' 형태이므로 콤마 제거
            price_str = str(raw_price).replace(",", "")
            # 2) float 변환
            price = float(price_str)
            data.append({"date": d.strftime("%Y-%m-%d"), "price": price})

        return JsonResponse({"data": data})

    except Exception as e:
        print("❌ price_data error:", e)
        return JsonResponse({"error": str(e)}, status=500)
