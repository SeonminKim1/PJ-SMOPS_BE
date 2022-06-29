from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MyGallerySerializer
from .models import Product as ProductModel

from rest_framework import status



# mygallery/
class MyGalleryAPIView(APIView):
    # 현재 접속한 유저가 가지고 있는 그림들
    def get(self, request):
        print("mygallery/ - GET 메서드 도착!")
        # # 필터적용 하여 시리얼라이저에 전달
        # price = request.query_params.get('price', '')
        # size = request.query_params.get('size', '')
        # products = ProductModel.objects.filter(owner_user_id="1")
        products = ProductModel.objects.all()
        print(products)
        
        return Response(MyGallerySerializer(products, many=True).data, status=status.HTTP_200_OK)
    
    
# mygallery/<product_id>
class MyGalleryInfoAPIView(APIView):
    # 게시물 상세보기(그림, 생성정보, 구매정보)
    def get(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        return Response(MyGallerySerializer(product), status=status.HTTP_200_OK)
    
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
        return Response(my_gallery_serializer, status=status.HTTP_200_OK)
    
    # 그림 삭제하기
    def delete(self, request, product_id):
        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return Response({"error" : "없는 상품 입니다."},
                                    status=status.HTTP_400_BAD_REQUEST)
        return Response()
        # return Response(my_gallery_serializer, status=status.HTTP_200_OK)


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
