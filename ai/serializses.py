from rest_framework import serializers
import boto3

from art.models import Product as ProductModel
from art.models import Log as LogModel

from .upload import UploadProduct

class AiLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogModel
        fields = "__all__"
        

class AiProductSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        return data
    
    def create(self, validated_data):
        url = UploadProduct.upload_s3(validated_data)
        
        # S3에 파일업로드 시 사용되는 URL을 DB에 저장
        validated_data["img_path"] = url
        product = ProductModel(**validated_data)
        product.save()
        
        return product
    
    log = AiLogSerializer(many=True, source="log_set", read_only=True)
    
    class Meta:
        model = ProductModel
        fields = ["id", "created_user", "owner_user", "img_path", "img_shape", "category", "title", "description",
                  "price", "is_selling", "created_date", "log"]



