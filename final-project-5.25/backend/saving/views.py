from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import requests
from .models import SavingProducts, SavingOptions
from .serializers import SavingProductsSerializer, SavingOptionsSerializer

API_KEY = settings.FINANCE_API_KEY
BASE_URL = "http://finlife.fss.or.kr/finlifeapi/"


@api_view(["GET", "POST"])
def saving_product(request):
    URL = BASE_URL + "savingProductsSearch.json"
    params = {"auth": API_KEY, "topFinGrpNo": "020000", "pageNo": 1}
    response = requests.get(URL, params=params).json()

    baseList = response["result"]["baseList"]
    optionList = response["result"]["optionList"]

    product_map = {}
    for data in baseList:
        fin_prdt_cd = data["fin_prdt_cd"]
        product, created = SavingProducts.objects.get_or_create(
            fin_prdt_cd=fin_prdt_cd,
            defaults={
                "kor_co_nm": data["kor_co_nm"],
                "fin_prdt_nm": data["fin_prdt_nm"],
                "etc_note": data["etc_note"],
                "join_deny": data["join_deny"],
                "join_member": data["join_member"],
                "join_way": data["join_way"],
                "spcl_cnd": data["spcl_cnd"],
            },
        )
        product_map[fin_prdt_cd] = product

    for option in optionList:
        fin_prdt_cd = option.get("fin_prdt_cd")
        product = product_map.get(fin_prdt_cd)
        if product:
            if not SavingOptions.objects.filter(
                product=product,
                fin_prdt_cd=option["fin_prdt_cd"],
                intr_rate_type_nm=option["intr_rate_type_nm"],
                save_trm=option["save_trm"],
            ).exists():
                SavingOptions.objects.create(
                    product=product,
                    fin_prdt_cd=option["fin_prdt_cd"],
                    intr_rate_type_nm=option["intr_rate_type_nm"],
                    intr_rate=option.get("intr_rate"),
                    intr_rate2=option.get("intr_rate2"),
                    save_trm=option["save_trm"],
                )

    if request.method == "GET":
        return JsonResponse({"response": response})

    return JsonResponse(
        {"message": "중복 제외 후 저장 완료"}, status=status.HTTP_201_CREATED
    )


@api_view(["GET", "POST"])
def deposit_product(request):
    """예금 상품 조회 및 저장"""
    URL = BASE_URL + "depositProductsSearch.json"
    params = {"auth": API_KEY, "topFinGrpNo": "020000", "pageNo": 1}
    response = requests.get(URL, params=params).json()

    baseList = response["result"]["baseList"]
    optionList = response["result"]["optionList"]

    product_map = {}
    for data in baseList:
        fin_prdt_cd = data["fin_prdt_cd"]
        product, created = SavingProducts.objects.get_or_create(
            fin_prdt_cd=fin_prdt_cd,
            defaults={
                "kor_co_nm": data["kor_co_nm"],
                "fin_prdt_nm": data["fin_prdt_nm"],
                "etc_note": data["etc_note"],
                "join_deny": data["join_deny"],
                "join_member": data["join_member"],
                "join_way": data["join_way"],
                "spcl_cnd": data["spcl_cnd"],
            },
        )
        product_map[fin_prdt_cd] = product

    for option in optionList:
        fin_prdt_cd = option.get("fin_prdt_cd")
        product = product_map.get(fin_prdt_cd)
        if product:
            if not SavingOptions.objects.filter(
                product=product,
                fin_prdt_cd=option["fin_prdt_cd"],
                intr_rate_type_nm=option["intr_rate_type_nm"],
                save_trm=option["save_trm"],
            ).exists():
                SavingOptions.objects.create(
                    product=product,
                    fin_prdt_cd=option["fin_prdt_cd"],
                    intr_rate_type_nm=option["intr_rate_type_nm"],
                    intr_rate=option.get("intr_rate"),
                    intr_rate2=option.get("intr_rate2"),
                    save_trm=option["save_trm"],
                )

    if request.method == "GET":
        return JsonResponse({"response": response})

    return JsonResponse(
        {"message": "예금 상품 저장 완료"}, status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
def combined_products(request):
    """적금과 예금 상품을 모두 가져오는 API 및 데이터베이스에 저장"""
    try:
        # --- Helper function for saving product and options ---
        def save_product_data(base_list_data, option_list_data):
            product_map = {}
            for data in base_list_data:
                fin_prdt_cd = data["fin_prdt_cd"]
                product, created = SavingProducts.objects.get_or_create(
                    fin_prdt_cd=fin_prdt_cd,
                    defaults={
                        "kor_co_nm": data.get("kor_co_nm"),
                        "fin_prdt_nm": data.get("fin_prdt_nm"),
                        "etc_note": data.get("etc_note"),
                        "join_deny": data.get("join_deny"),
                        "join_member": data.get("join_member"),
                        "join_way": data.get("join_way"),
                        "spcl_cnd": data.get("spcl_cnd"),
                    },
                )
                # If product already existed, we might want to update it,
                # but get_or_create with defaults only sets them on creation.
                # For simplicity, matching original saving_product behavior.
                product_map[fin_prdt_cd] = product

            for option in option_list_data:
                fin_prdt_cd = option.get("fin_prdt_cd")
                product = product_map.get(fin_prdt_cd)
                if product:
                    if not SavingOptions.objects.filter(
                        product=product,
                        intr_rate_type_nm=option["intr_rate_type_nm"],
                        save_trm=option["save_trm"],
                    ).exists():
                        SavingOptions.objects.create(
                            product=product,
                            fin_prdt_cd=option["fin_prdt_cd"],
                            intr_rate_type_nm=option["intr_rate_type_nm"],
                            intr_rate=option.get("intr_rate"),
                            intr_rate2=option.get("intr_rate2"),
                            save_trm=option["save_trm"],
                        )

        # --- End of helper function ---

        # 적금 상품 가져오기 및 저장
        saving_url = BASE_URL + "savingProductsSearch.json"
        saving_params = {"auth": API_KEY, "topFinGrpNo": "020000", "pageNo": 1}
        saving_response_json = requests.get(saving_url, params=saving_params).json()
        save_product_data(
            saving_response_json["result"]["baseList"],
            saving_response_json["result"]["optionList"],
        )

        # 예금 상품 가져오기 및 저장
        deposit_url = BASE_URL + "depositProductsSearch.json"
        deposit_params = {"auth": API_KEY, "topFinGrpNo": "020000", "pageNo": 1}
        deposit_response_json = requests.get(deposit_url, params=deposit_params).json()
        save_product_data(
            deposit_response_json["result"]["baseList"],
            deposit_response_json["result"]["optionList"],
        )

        # 프론트엔드에 반환할 데이터 구성 (API 응답 기반)
        saving_products_for_response = saving_response_json["result"]["baseList"]
        for product in saving_products_for_response:
            product["product_type"] = "적금"

        deposit_products_for_response = deposit_response_json["result"]["baseList"]
        for product in deposit_products_for_response:
            product["product_type"] = "예금"

        combined_products_list_for_response = (
            saving_products_for_response + deposit_products_for_response
        )
        combined_options_list_for_response = (
            saving_response_json["result"]["optionList"]
            + deposit_response_json["result"]["optionList"]
        )

        return JsonResponse(
            {
                "response": {
                    "result": {
                        "baseList": combined_products_list_for_response,
                        "optionList": combined_options_list_for_response,
                    }
                }
            }
        )

    except Exception as e:
        import traceback

        print(f"❌ combined_products error: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse(
            {"error": f"상품 조회 중 오류가 발생했습니다: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def option_list(request, fin_prdt_cd):
    options = SavingOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = SavingOptionsSerializer(options, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_detail(request, fin_prdt_cd):
    try:
        product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        serializer = SavingProductsSerializer(product)
        return Response(serializer.data)
    except SavingProducts.DoesNotExist:
        return Response(
            {"message": "해당 상품이 없습니다."}, status=status.HTTP_404_NOT_FOUND
        )
