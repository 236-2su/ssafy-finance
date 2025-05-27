import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import pandas as pd  # pd is not defined 오류 수정을 위해 추가
import yfinance as yf
from datetime import datetime, timedelta


@require_GET
def price_data(request):
    """
    GET parameters:
      - asset: 'gold' 또는 'silver'
      - start_date: 'YYYY-MM-DD' (선택)
      - end_date: 'YYYY-MM-DD' (선택)
    """
    asset_param = request.GET.get("asset")
    start_str = request.GET.get("start_date")
    end_str = request.GET.get("end_date")

    ticker_map = {
        "gold": "GC=F",
        "silver": "SI=F",
    }
    if asset_param not in ticker_map:
        return JsonResponse({"error": "Invalid asset"}, status=400)

    ticker_symbol = ticker_map[asset_param]

    # 날짜 기본값 설정 및 end_date 조정
    # yfinance는 end_date를 exclusive하게 처리하는 경향이 있으므로,
    # 사용자가 입력한 날짜까지 포함시키기 위해 하루 뒤로 설정합니다.
    if end_str:
        try:
            end_dt_adjusted = datetime.strptime(end_str, "%Y-%m-%d") + timedelta(days=1)
            end_str_adjusted = end_dt_adjusted.strftime("%Y-%m-%d")
        except ValueError:
            return JsonResponse(
                {"error": "Invalid end_date format. Please use YYYY-MM-DD."}, status=400
            )
    else:
        # end_date가 없으면 오늘 날짜 + 1일로 설정
        end_dt_adjusted = datetime.today() + timedelta(days=1)
        end_str_adjusted = end_dt_adjusted.strftime("%Y-%m-%d")

    if start_str:
        try:
            # 시작 날짜 유효성 검사
            datetime.strptime(start_str, "%Y-%m-%d")
        except ValueError:
            return JsonResponse(
                {"error": "Invalid start_date format. Please use YYYY-MM-DD."},
                status=400,
            )
    else:
        # start_date가 없으면 조정된 end_date로부터 1년 전으로 설정
        start_dt_default = datetime.strptime(end_str_adjusted, "%Y-%m-%d") - timedelta(
            days=366
        )  # 1년 + 하루 전
        start_str = start_dt_default.strftime("%Y-%m-%d")

    print(f"Fetching data for {ticker_symbol} from {start_str} to {end_str_adjusted}")

    try:
        tick = yf.Ticker(ticker_symbol)
        # auto_adjust=True를 사용하면 'Adj Close'가 'Close'가 되고, 분할/배당 등이 조정된 가격을 사용합니다.
        # 여기서는 순수 종가를 원하므로 auto_adjust=False로 하고, 'Close' 컬럼을 명시적으로 사용하거나,
        # auto_adjust=True를 쓰고 반환되는 'Close' (실제로는 조정된 종가)를 사용합니다.
        # 일반적으로 금융 차트에서는 조정된 종가를 사용하는 것이 일반적입니다.
        data_df = tick.history(start=start_str, end=end_str_adjusted, auto_adjust=True)

        if data_df.empty:
            return JsonResponse(
                {"data": [], "message": "No data found for the given period."},
                status=200,
            )

        # 'Date' 인덱스를 컬럼으로 변환하고 필요한 컬럼만 선택
        data_df.reset_index(inplace=True)
        # yfinance는 'Date' (UTC)와 'Close' 컬럼을 반환 (auto_adjust=True 시)
        # 필요한 경우 시간대 변환: data_df['Date'] = data_df['Date'].dt.tz_convert('Asia/Seoul')
        # 하지만 날짜만 사용할 것이므로 시간대는 크게 중요하지 않을 수 있음

        # 컬럼명 변경 (프론트엔드 호환성) 및 데이터 포맷팅
        processed_data = []
        for index, row in data_df.iterrows():
            # yfinance에서 Date는 이미 datetime 객체일 수 있음 (인덱스에서 변환 시)
            # 또는 Timestamp 객체일 수 있음
            date_obj = row["Date"]
            # NaT (Not a Time) 체크
            if pd.isna(date_obj):
                continue

            processed_data.append(
                {
                    "date": date_obj.strftime("%Y-%m-%d"),
                    "price": round(row["Close"], 2) if pd.notna(row["Close"]) else None,
                }
            )

        # price가 None인 항목 제거
        processed_data = [item for item in processed_data if item["price"] is not None]

        return JsonResponse({"data": processed_data})

    except Exception as e:
        print(f"❌ yfinance data fetching error for {ticker_symbol}: {e}")
        # 보다 구체적인 오류 메시지를 사용자에게 전달할 수 있도록 고려
        return JsonResponse(
            {"error": f"Failed to fetch data from yfinance: {str(e)}"}, status=500
        )
