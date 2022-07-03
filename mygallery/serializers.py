from rest_framework import serializers

from art.models import Product as ProductModel
from art.models import Log as LogModel


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogModel
        fields = ["product", "old_owner", "updated_date", "old_price", ]

class MyGallerySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        img_path = validated_data["img_path"]
        
        # S3 에 파일 업로드
        instance = FileUpload()
        result = instance.file_upload(img_path)
        print(result["success"])
        
        # S3에 파일업로드 시 사용되는 URL을 DB에 저장
        validated_data["img_path"] = f"luckyseven-todaylunch.s3.ap-northeast-2.amazonaws.com/{img_path}"
        product = ProductModel(**validated_data)
        product.save()
        
        return product
    
    log = LogSerializer(many=True, source="log_set", read_only=True)
    
    class Meta:
        model = ProductModel
        fields = ["id", "category", "created_user", "img_path", "title", "description",
                  "price", "is_selling", "created_date", "log"]


