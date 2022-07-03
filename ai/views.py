from PIL import Image
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializses import AiProductSerializer
from .serializses import AiLogSerializer
from art.models import Product as ProductModel

from .upload import UploadProduct

# ai/
class AiProductView(APIView):
    def get(self, request):
        product = ProductModel.objects.get(id=17)
        return Response(AiProductSerializer(product).data)

    # 상품 등록
    def post(self, request):
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

# ai/inference/
class AiCreateProductView(APIView):
    def post(self, request):
        content = request.data["content"]
        style = [request.data["style"]]
        print(type(content))
        print(type(style))

        output_image = UploadProduct.create_product(content, style)
        from django.http import HttpResponse

        response = HttpResponse(content_type='image/png')
        output_image.save(response, "PNG")
        print(response)
        return response