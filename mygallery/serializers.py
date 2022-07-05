from rest_framework import serializers

from art.models import Product as ProductModel
from art.models import Log as LogModel


class LogSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    def get_product(self, obj):
        return obj.product.title

    old_owner = serializers.SerializerMethodField()
    def get_old_owner(self, obj):
        return obj.old_owner.fullname

    class Meta:
        model = LogModel
        fields = ["product", "old_owner", "updated_date", "old_price", ]


class MyGallerySerializer(serializers.ModelSerializer):
    created_user = serializers.SerializerMethodField()
    def get_created_user(self, obj):
        return obj.created_user.fullname
    
    category = serializers.SerializerMethodField()
    def get_category(self, obj):
        return obj.category.name
    
    img_shape = serializers.SerializerMethodField()
    def get_img_shape(self, obj):
        return obj.img_shape.shape

    def create(self, validated_data):
        img_path = validated_data["img_path"]

        # S3 에 파일 업로드
        instance = FileUpload()
        result = instance.file_upload(img_path)
        print(result["success"])

        # S3에 파일업로드 시 사용되는 URL을 DB에 저장
        validated_data[
            "img_path"] = f"luckyseven-todaylunch.s3.ap-northeast-2.amazonaws.com/{img_path}"
        product = ProductModel(**validated_data)
        product.save()

        return product

    log = LogSerializer(many=True, source="log_set")

    class Meta:
        model = ProductModel
        fields = ["id", "category", "created_user", "img_path", "title", "description",
                  "price", "is_selling", "created_date","img_shape", "log"]
