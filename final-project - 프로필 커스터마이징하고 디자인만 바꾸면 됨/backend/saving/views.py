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
