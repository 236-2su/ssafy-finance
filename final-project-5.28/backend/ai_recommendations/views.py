import os
from dotenv import load_dotenv
from openai import OpenAI
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from saving.models import (
    SavingProducts,
)
import traceback

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("!!!!!!!!!! OpenAI API Key is NOT SET in .env file !!!!!!!!!!")
else:
    # 실제 키 값의 일부만 마스킹하여 출력 (보안을 위해 전체 키 출력은 피함)
    masked_key = (
        OPENAI_API_KEY[:8] + "..." * (len(OPENAI_API_KEY) > 12) + OPENAI_API_KEY[-4:]
    )
    print(f"!!!!!!!!!! Loaded OpenAI API Key (masked): {masked_key} !!!!!!!!!!")
client = OpenAI(api_key=OPENAI_API_KEY)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_ai_recommendation(request):
    user = request.user

    if not user.survey_completed or not (
        user.stock_experience
        or user.investment_style
        or user.monthly_investment_amount
        or user.investment_goal
    ):
        return Response(
            {"error": "AI 추천을 받으려면 먼저 투자 성향 설문조사를 완료해주세요."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    survey_details = []
    if user.stock_experience:
        survey_details.append(f"주식 투자 경험: {user.get_stock_experience_display()}")
    if user.investment_style:
        survey_details.append(f"투자 성향: {user.get_investment_style_display()}")
    if user.monthly_investment_amount:
        survey_details.append(
            f"월 투자 가능 금액: {user.get_monthly_investment_amount_display()}"
        )
    if user.investment_goal:
        survey_details.append(f"투자 목표: {user.get_investment_goal_display()}")
    survey_summary = ", ".join(survey_details)

    recommended_savings = []
    all_savings = SavingProducts.objects.all()
    db_recommended_savings = list(all_savings[:2])
    for sp in db_recommended_savings:
        options = sp.savingoptions_set.order_by("-intr_rate2")
        highest_option = options.first()
        if highest_option:
            recommended_savings.append(
                {
                    "id": sp.id,
                    "fin_prdt_cd": sp.fin_prdt_cd,  # [수정] fin_prdt_cd 추가
                    "fin_prdt_nm": sp.fin_prdt_nm,
                    "kor_co_nm": sp.kor_co_nm,
                    "intr_rate2": highest_option.intr_rate2,
                    "intr_rate": highest_option.intr_rate,
                    "intr_rate_type_nm": highest_option.intr_rate_type_nm,
                    "save_trm": highest_option.save_trm,
                    "rsrv_type_nm": (
                        highest_option.rsrv_type_nm
                        if hasattr(highest_option, "rsrv_type_nm")
                        else None
                    ),  # 적금의 경우 필요할 수 있음
                }
            )

    stock_prompt_text = f"이 사용자의 투자 설문 조사 결과는 다음과 같습니다: {survey_summary}. 이 설문 조사 결과를 최우선으로 고려하여, 투자할 만한 주식 종목 3가지와 그 이유를 간략히 추천해주세요. 각 추천은 종목명, 추천 이유 형식으로 명확히 구분해주세요. 각 추천 항목은 '종목명: [이름]\n추천 이유: [설명]' 형태로 제공하고, 각 항목 사이에는 빈 줄 하나로 구분해주세요."
    ai_stock_recommendation_text = "AI 주식 추천 정보를 가져오지 못했습니다."

    print("Attempting AI Stock Recommendation...")
    # API 키가 실제로 client 객체에 어떻게 설정되었는지 확인 (주의: 실제 키가 로그에 남을 수 있음 - 테스트 후 제거)
    # print(f"OpenAI client API Key: {client.api_key}")
    print(
        f"Using environment OpenAI API Key (masked): {'SET' if OPENAI_API_KEY else 'NOT SET'}"
    )
    if OPENAI_API_KEY:
        print(
            f"Value from os.environ (masked): {OPENAI_API_KEY[:8] + '...' * (len(OPENAI_API_KEY) > 12) + OPENAI_API_KEY[-4:]}"
        )

    print(f"Prompt for AI: {stock_prompt_text}")

    try:
        chat_completion_stock = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": stock_prompt_text,
                }
            ],
            model="gpt-4o-mini",
            timeout=20.0,
        )
        ai_stock_recommendation_text = chat_completion_stock.choices[0].message.content
        print("AI Stock Recommendation successful.")
    except Exception as e:
        print(
            f"!!!!!!!!!! AI 주식 추천 중 명시적 오류 발생 !!!!!!!!!!: {type(e).__name__} - {str(e)}"
        )
        traceback.print_exc()
        ai_stock_recommendation_text = "AI 주식 추천을 가져오는 중 오류가 발생했습니다. (상세 오류는 서버 로그 확인)"

    return Response(
        {
            "saving_products": recommended_savings,
            "stock_recommendations_ai": ai_stock_recommendation_text,
        },
        status=status.HTTP_200_OK,
    )
