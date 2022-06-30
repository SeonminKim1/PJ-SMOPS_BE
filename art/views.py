from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MyGallerySerializer
from .models import Product as ProductModel
from .models import User as UserModel

from rest_framework import status

from .models import Product

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
        # return Response(my_gallery_serializer, status=status.HTTP_200_OK)

