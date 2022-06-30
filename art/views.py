from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404

from .serializers import MyGallerySerializer
from .serializers import ProductsMainSerializer

from .models import Product as ProductModel
from .models import User as UserModel
from .models import Product, Category, Log, ImageShape
from user.models import User

# Query Debugger용
from _utils.query_utils import query_debugger

################################################
##### Main
# product/<category_name>/
class ProductsByCategoryView(APIView):
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

# product/<category_name><filters..>
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

################################################
##### My Gallery
# art/product/
class ProductAPIView(APIView):
    # 상품 등록
    def post(self, request):
        # request.data["created_user"] = request.user
        # request.data["owner_user"] = request.user
        # request.data["created_user"] = UserModel.objects.get(id=1).id
        print(request.data)
        product_serializer = MyGallerySerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data, status=status.HTTP_200_OK)


# art/mygallery/
class MyGalleryAPIView(APIView):
    # 현재 접속한 유저가 가지고 있는 그림들
    def get(self, request):
        # # 필터적용 하여 시리얼라이저에 전달
        # price = request.query_params.get('price', '')
        # size = request.query_params.get('size', '')
        products = ProductModel.objects.filter(owner_user_id="1")        
        return Response(MyGallerySerializer(products, many=True).data, status=status.HTTP_200_OK)
        
        
# art/mygallery/<product_id>
class MyGalleryInfoAPIView(APIView):
    # 게시물 상세보기(그림, 생성정보, 구매정보)
    def get(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        return Response(MyGallerySerializer(product, data=request.data), status=status.HTTP_200_OK)
    
    # 판매 현황 수정
    def put(self, request, product_id):
        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return Response({"error" : "없는 상품 입니다."},
                                    status=status.HTTP_400_BAD_REQUEST)
        my_gallery_serializer = MyGallerySerializer(product, data=request.data, partial=True)
        my_gallery_serializer.is_valid(raise_exception=True)
        my_gallery_serializer.save()
        return Response(my_gallery_serializer.data, status=status.HTTP_200_OK)
    
    # 그림 삭제하기
    def delete(self, request, product_id):
        try:
            product = ProductModel.objects.get(id=product_id).delete()
        except ProductModel.DoesNotExist:
            return Response({"error" : "없는 상품 입니다."},
                                    status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"result": "상품이 삭제되었습니다."}, status=status.HTTP_200_OK)

