from rest_framework import serializers

from art.models import Product as ProductModel
from art.models import Log as LogModel


class AiProductSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="fullname")

    def validate(self, data):
        return data

    def create(self, validated_data):
        product = ProductModel(**validated_data)
        product.save()

        return product

    class Meta:
        model = ProductModel
        fields = [
            "created_user",
            "owner_user",
            "img_path",
            "img_shape",
            "category",
            "title",
            "description",
            "price",
            "is_selling",
        ]