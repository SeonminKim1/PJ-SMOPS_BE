# Create your views here.
from rest_framework import viewsets, permissions, status, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.db.models import Q

from user.models import User
from .models import Product, Category, Log, ImageShape
from .serializers import ProductsMainSerializer

# Query Debugger용
from _utils.query_utils import query_debugger

class ProductsByCategoryView(APIView):
    # 일반 get => redirect()
    @query_debugger
    def get(self, request, category_name):
        # get - Category by Category_name
        try:
            category = Category.objects.get(name = category_name)
        except Category.DoesNotExist:
            return Response({"message": "invalid Category type"}, status=status.HTTP_400_BAD_REQUEST)
        # filter - Products by category_id
        products = Product.objects.filter(category_id = category, is_selling=True)
        # print('==products queryset data ', products)

        products_serializers = ProductsMainSerializer(products, many=True).data
        # products = Product.objects.all()
        return Response(products_serializers, status.HTTP_200_OK)

class ProductsByFilteringView(APIView):
    @query_debugger
    def get(self, request):
        # 1. get Request(GET) Params
        category_name = request.query_params.get('category_name', '인물화')
        price = request.query_params.get('price', "0~10000000만원")
        image_shape = request.query_params.get('image_shape', '정방형')
        searching_text = request.query_params.get('searching_text', '')
        ordering = request.query_params.get('ordering', 'latest_date') # latest_date, price_up, price_down
        print('==requset data', category_name, '///', price, '///', image_shape, '///', searching_text, '///', ordering)

        # 2-1. Get Price Range
        min_price, max_price = price.replace('만원', '').split('~')
        # print('=== min_max_price', min_price, max_price)

        # 2-2. Check Category Model - 3
        try:
            category = Category.objects.get(name = category_name)
        except Category.DoesNotExist:
            return Response({"message": "invalid Category type"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 2-3. Check Imageshape Model -1
        try:
            img_shape = ImageShape.objects.get(shape = image_shape) 
        except ImageShape.DoesNotExist:
            return Response({"message": "invalid ImageShape"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 2-4. get Artist searching list - ex) '김'을 가진 user id list - 1
        searching_user_id_list = [user.id for user in User.objects.filter(fullname__contains = searching_text)] # queryset list (name)
        print('===searching_user_id_list', searching_user_id_list)

        # 3. get Product - 0
        products = Product.objects.filter(
                Q(category_id = category) & Q(is_selling=True) &
                Q(price__gte=min_price) & Q(price__lt=max_price) &
                Q(img_shape_id = img_shape) &
                Q(created_user_id__in = searching_user_id_list)
        )

        # 4. Product ordering - 0
        if ordering == '':
            pass
        elif ordering == 'price_down': # 가격 내림 차 순
            products = products.order_by('-price')
        elif ordering == 'price_up': # 가격 오름 차 순
            products = products.order_by('price')
        elif ordering == 'latest_date': # 최신 날짜순
            products = products.order_by('-created_date')

        # 5. Product Serializing - 9
        products_serializers = ProductsMainSerializer(products, many=True).data
        return Response(products_serializers, status.HTTP_200_OK)

# Test 용 CBV 입니다. endpoint : get_products/
class TestProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        
        print(products)
        return Response({}, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = BookSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save() # create() 호출함.
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
