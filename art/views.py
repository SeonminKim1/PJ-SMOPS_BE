from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.db import transaction

from .serializers import ProductsMainSerializer, ProductsDeatilSerializer

from .models import Product, Category, Log, ImageShape
from user.models import User

# Query Debugger용
from _utils.query_utils import query_debugger

################################################
##### Main
# product/<category_name>/
class ProductsByCategoryView(APIView):
    @query_debugger
    @transaction.atomic()
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
        print('====', products_serializers)
        # products = Product.objects.all()
        return Response(products_serializers, status.HTTP_200_OK)

# product/<category_name><filters..>
class ProductsByFilteringView(APIView):
    @query_debugger
    @transaction.atomic()
    def get(self, request):
        # 1. get Request(GET) Params
        category_name = request.query_params.get('category_name')
        category_name = '인물화' if category_name == '' else category_name

        price = request.query_params.get('price')
        image_shape = request.query_params.get('image_shape') 
        ordering = request.query_params.get('ordering_value') # latest_date, price_up, price_down

        print('==requset data', category_name, '///', price, '///', image_shape, '///', ordering)

        # 2-2. Check Category Model - 3
        try:
            category = Category.objects.get(name = category_name)
        except Category.DoesNotExist:
            return Response({"message": "invalid Category type"}, status=status.HTTP_400_BAD_REQUEST)

        # 2-3. Check Imageshape Model -1
        if image_shape !='':
            try:
                img_shape = ImageShape.objects.get(shape = image_shape) 
            except ImageShape.DoesNotExist:
                return Response({"message": "invalid ImageShape"}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Make Queries by Filter condition - 0
        q = Q()
        q.add(Q(is_selling=True), q.AND)
        q.add(Q(category_id = category), q.AND)
        if price!='':
            min_price, max_price = price.replace('원', '').replace(',', '').split('~')
            q.add(Q(price__gte=min_price), q.AND)
            if max_price != 'infinite':
                Q(price__lt=max_price)
        if image_shape !='':
            q.add(Q(img_shape_id = img_shape), q.AND)

        products = Product.objects.filter(q)
        # 4. Product ordering - 0
        if ordering == '':
            pass
        elif ordering == 'descending_price': # 가격 내림 차 순
            print('가격 내림차순')
            products = products.order_by('-price')
        elif ordering == 'ascending_price': # 가격 오름 차 순
            products = products.order_by('price')
            print('가격 오름 차순')
        elif ordering == 'latest_date': # 최신 날짜순
            products = products.order_by('-created_date')
            print('가격 최신 날짜순')

        # 5. Product Serializing - 9
        products_serializers = ProductsMainSerializer(products, many=True).data
        return Response(products_serializers, status.HTTP_200_OK)

# product/<category_name><searching_text>
class ProductsByArtistSearchingingView(APIView):
    @query_debugger
    @transaction.atomic()
    def get(self, request, category_name, searching_text):
        # 1. get Request(GET) Params
        #category_name = request.query_params.get('category_name', '인물화')
        #searching_text = request.query_params.get('searching_text', '')
        print('==requset data', category_name, '///', searching_text)

        # 2-1. Check Category Model - 3
        try:
            category = Category.objects.get(name = category_name)
        except Category.DoesNotExist:
            return Response({"message": "invalid Category type"}, status=status.HTTP_400_BAD_REQUEST)
                
        # 2-2. get Artist searching list - ex) '김'을 가진 user id list - 1
        searching_user_id_list = [user.id for user in User.objects.filter(fullname__contains = searching_text)] # queryset list (name)
        print('===searching_user_id_list', searching_user_id_list)

        # 3. get Product - 0
        products = Product.objects.filter(
                Q(category_id = category) & Q(is_selling=True) &
                Q(created_user_id__in = searching_user_id_list)
        )

        # 4. Product Serializing - 9
        products_serializers = ProductsMainSerializer(products, many=True).data
        return Response(products_serializers, status.HTTP_200_OK)

# product/detail/<int:product_id>
class ProductDetailsView(APIView):
    @query_debugger
    @transaction.atomic()
    def get(self, request, product_id):
        # 1. get Request(GET) Params
        #category_name = request.query_params.get('category_name', '인물화')
        #searching_text = request.query_params.get('searching_text', '')
        print('==requset data', product_id)

        # 2. get Product Object
        try:
            product = Product.objects.get(id = product_id)
        except Product.DoesNotExist:
            return Response({"message": "invalid Product type"}, status=status.HTTP_400_BAD_REQUEST)

        # 4. Product Serializing - 9
        product_serializers = ProductsDeatilSerializer(product).data
        return Response(product_serializers, status.HTTP_200_OK)

# product/detail/buy/log
class ProductDetailsBuyView(APIView):
    @query_debugger
    @transaction.atomic()
    def post(self, request):
        # 1. get Request(POST) Params
        product_id = request.data['product_id']
        price = request.data['price']
        updated_date = request.data['updated_date']
        user = request.user

        # 2. 구매했으면 상품 소유자 변경
        product = Product.objects.get(id = product_id)
        product.owner_user = user
        product.is_seliing = False
        product.save()

        # 3. 로그 추가
        Log.objects.create(product=product, old_owner=user, updated_date= updated_date, old_price=price)
        return Response({'message':'Success'}, status.HTTP_200_OK)
