from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import MyGallerySerializer

from art.models import Product as ProductModel


# Query Debugger용
from _utils.query_utils import query_debugger

# mygallery/
class MyGalleryAPIView(APIView):
    # 현재 접속한 유저가 가지고 있는 그림들
    def get(self, request):
        # 필터적용 하여 시리얼라이저에 전달

        # 현재 접속중인 유저가 가진 작품들만 출력
        products = ProductModel.objects.filter(owner_user_id=request.user.id)
        return Response(MyGallerySerializer(products, many=True).data, status=status.HTTP_200_OK)


# mygallery/<product_id>
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
            return Response({"error": "없는 상품 입니다."},
                            status=status.HTTP_400_BAD_REQUEST)
        my_gallery_serializer = MyGallerySerializer(
            product, data=request.data, partial=True)
        my_gallery_serializer.is_valid(raise_exception=True)
        my_gallery_serializer.save()
        return Response(my_gallery_serializer.data, status=status.HTTP_200_OK)

    # 그림 삭제하기
    def delete(self, request, product_id):
        try:
            product = ProductModel.objects.get(id=product_id).delete()
        except ProductModel.DoesNotExist:
            return Response({"error": "없는 상품 입니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"result": "작품이 삭제되었습니다."}, status=status.HTTP_200_OK)
