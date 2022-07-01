from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializses import AiProductSerializer
from .serializses import AiLogSerializer
from art.models import Product as ProductModel

class AiProductView(APIView):
    def get(self, request):
        product = ProductModel.objects.get(id=16)
        return Response(AiProductSerializer(product).data)

    # 상품 등록
    def post(self, request):
        request.data["created_user"] = request.user.id
        request.data["owner_user"] = request.user.id        
        product_serializer = AiProductSerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()

        # 최초 로그 기록
        request.data["product"] = product_serializer.data["id"]
        request.data["old_owner"] = product_serializer.data["created_user"]
        request.data["old_price"] = product_serializer.data["price"]
        log_serializer = AiLogSerializer(data=request.data)
        log_serializer.is_valid(raise_exception=True)
        log_serializer.save()
        
        return Response(product_serializer.data, status=status.HTTP_200_OK)


        