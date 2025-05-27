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


from django.db.models import Max, Subquery, OuterRef

@api_view(["GET"])
def combined_products(request):
    """적금과 예금 상품을 모두 가져오고 정렬하는 API"""
    try:
        # --- Helper function for saving product and options ---
        # (이전과 동일, 외부 API 호출 및 DB 저장은 유지)
        def save_product_data(base_list_data, option_list_data, product_type_value):
            product_map = {}
            for data in base_list_data:
                fin_prdt_cd = data["fin_prdt_cd"]
                # product_type 필드가 SavingProducts 모델에 없으므로, 여기서는 저장하지 않음
                # 필요하다면 모델 수정 후 여기에 product_type=product_type_value 추가
                product, created = SavingProducts.objects.update_or_create(
                    fin_prdt_cd=fin_prdt_cd,
                    defaults={
                        "kor_co_nm": data.get("kor_co_nm"),
                        "fin_prdt_nm": data.get("fin_prdt_nm"),
                        "etc_note": data.get("etc_note"),
                        "join_deny": data.get("join_deny"),
                        "join_member": data.get("join_member"),
                        "join_way": data.get("join_way"),
                        "spcl_cnd": data.get("spcl_cnd"),
                        # views와 recommendations는 다른 로직으로 업데이트되므로 여기서는 제외
                    },
                )
                product_map[fin_prdt_cd] = product

            for option in option_list_data:
                fin_prdt_cd = option.get("fin_prdt_cd")
                product = product_map.get(fin_prdt_cd)
                if product:
                    SavingOptions.objects.update_or_create(
                        product=product,
                        fin_prdt_cd=option["fin_prdt_cd"], # 중복 방지를 위해 fin_prdt_cd도 조건에 추가
                        intr_rate_type_nm=option["intr_rate_type_nm"],
                        save_trm=option["save_trm"],
                        defaults={
                            "intr_rate": option.get("intr_rate"),
                            "intr_rate2": option.get("intr_rate2"),
                        }
                    )
        # --- End of helper function ---

        # 적금 상품 가져오기 및 저장
        saving_url = BASE_URL + "savingProductsSearch.json"
        saving_params = {"auth": API_KEY, "topFinGrpNo": "020000", "pageNo": 1}
        saving_response_json = requests.get(saving_url, params=saving_params).json()
        save_product_data(
            saving_response_json["result"]["baseList"],
            saving_response_json["result"]["optionList"],
            "적금" # product_type 전달
        )

        # 예금 상품 가져오기 및 저장
        deposit_url = BASE_URL + "depositProductsSearch.json"
        deposit_params = {"auth": API_KEY, "topFinGrpNo": "020000", "pageNo": 1}
        deposit_response_json = requests.get(deposit_url, params=deposit_params).json()
        save_product_data(
            deposit_response_json["result"]["baseList"],
            deposit_response_json["result"]["optionList"],
            "예금" # product_type 전달
        )

        # DB에서 상품 목록 가져오기
        sort_by = request.GET.get("sort_by", "default")  # 기본 정렬: id (혹은 pk)
        
        products_queryset = SavingProducts.objects.all()

        if sort_by == "recommendations":
            products_queryset = products_queryset.order_by("-recommendations", "-pk")
        elif sort_by == "views":
            products_queryset = products_queryset.order_by("-views", "-pk")
        elif sort_by == "interest_rate":
            # 각 상품별 최고 우대금리(intr_rate2)를 계산하여 정렬
            # SavingOptions에서 해당 product의 가장 높은 intr_rate2를 가져옴
            # 만약 intr_rate2가 null인 경우를 대비하여 -1과 같은 낮은 값으로 처리 (또는 Coalesce 사용)
            # 주의: 이 방식은 DB에 따라 성능 이슈가 있을 수 있음. 데이터 양이 많다면 최적화 필요.
            highest_rate_subquery = SavingOptions.objects.filter(
                product=OuterRef('pk')
            ).order_by('-intr_rate2').values('intr_rate2')[:1]
            
            products_queryset = products_queryset.annotate(
                max_intr_rate2=Subquery(highest_rate_subquery)
            ).order_by("-max_intr_rate2", "-pk")
        else: # 기본 정렬 (랜덤) 또는 알 수 없는 sort_by 값
            products_queryset = products_queryset.order_by("?")


        serializer = SavingProductsSerializer(products_queryset, many=True)
        
        # product_type 정보를 추가 (API 응답을 활용하거나, 모델에 필드 추가 후 serializer에서 처리)
        # 현재는 API 응답을 기반으로 product_type을 매핑합니다.
        # 이는 DB에 product_type이 없다는 가정 하에 임시 방편입니다.
        # 이상적으로는 SavingProducts 모델에 product_type 필드를 추가하고,
        # save_product_data에서 저장하며, serializer에서 이를 포함해야 합니다.
        
        # API 응답에서 fin_prdt_cd를 키로 product_type을 매핑
        product_type_map = {}
        for p_data in saving_response_json["result"]["baseList"]:
            product_type_map[p_data["fin_prdt_cd"]] = "적금"
        for p_data in deposit_response_json["result"]["baseList"]:
            product_type_map[p_data["fin_prdt_cd"]] = "예금"

        serialized_data = []
        for product_data in serializer.data:
            # Serializer.data는 이미 딕셔너리 리스트입니다.
            # 각 딕셔너리에 product_type을 추가합니다.
            fin_prdt_cd = product_data.get("fin_prdt_cd")
            product_data["product_type"] = product_type_map.get(fin_prdt_cd, "정보 없음") # 매핑 실패 시 기본값
            serialized_data.append(product_data)
            
        # 옵션 데이터도 함께 반환 (기존 로직 유지)
        # 정렬된 상품 목록에 맞춰 옵션도 필터링하거나 할 필요는 현재 요구사항에 없음
        combined_options_list_for_response = (
            saving_response_json["result"]["optionList"]
            + deposit_response_json["result"]["optionList"]
        )

        return Response( # JsonResponse 대신 DRF Response 사용
            {
                # "result" 키를 유지하여 프론트엔드 호환성 고려
                "result": {
                    "baseList": serialized_data, 
                    "optionList": combined_options_list_for_response 
                }
            }
        )

    except Exception as e:
        import traceback
        print(f"❌ combined_products error: {str(e)}")
        print(traceback.format_exc())
        return Response( # JsonResponse 대신 DRF Response 사용
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
