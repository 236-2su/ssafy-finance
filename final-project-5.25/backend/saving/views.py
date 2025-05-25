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
    """적금과 예금 상품을 모두 가져오는 API"""
    try:
        # 적금 상품 가져오기
        saving_url = BASE_URL + "savingProductsSearch.json"
        saving_params = {"auth": API_KEY, "topFinGrpNo": "020000", "pageNo": 1}
        saving_response = requests.get(saving_url, params=saving_params).json()
        
        # 예금 상품 가져오기
        deposit_url = BASE_URL + "depositProductsSearch.json"
        deposit_params = {"auth": API_KEY, "topFinGrpNo": "020000", "pageNo": 1}
        deposit_response = requests.get(deposit_url, params=deposit_params).json()
        
        # 적금 상품에 타입 추가
        saving_products = saving_response["result"]["baseList"]
        for product in saving_products:
            product["product_type"] = "적금"
            
        # 예금 상품에 타입 추가
        deposit_products = deposit_response["result"]["baseList"]
        for product in deposit_products:
            product["product_type"] = "예금"
        
        # 두 상품 리스트 합치기
        combined_products = saving_products + deposit_products
        
        # 옵션 리스트도 합치기
        saving_options = saving_response["result"]["optionList"]
        deposit_options = deposit_response["result"]["optionList"]
        combined_options = saving_options + deposit_options
        
        return JsonResponse({
            "response": {
                "result": {
                    "baseList": combined_products,
                    "optionList": combined_options
                }
            }
        })
        
    except Exception as e:
        return JsonResponse(
            {"error": f"상품 조회 중 오류가 발생했습니다: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
