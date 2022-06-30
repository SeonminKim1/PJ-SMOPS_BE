from rest_framework import serializers

from art.models import Category as CategoryModel, Product
from art.models import Product as ProductModel
from art.models import Log as LogModel
from art.models import ImageShape as ImageShapeModel

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["name"]


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogModel
        fields = ["product", "old_owner", "updated_date", "old_price", ]


class MyGallerySerializer(serializers.ModelSerializer):
    created_user = serializers.SerializerMethodField()
    def get_created_user(self, obj):
        return obj.created_user.fullname
    
    owner_user = serializers.SerializerMethodField()
    def get_owner_user(self, obj):
        return obj.owner_user.fullname
    
    category = serializers.SerializerMethodField()
    def get_category(self,obj):
        return obj.category.name
    
    log = LogSerializer(many=True, source="log_set")
    
    class Meta:
        model = ProductModel
        fields = ["created_user", "owner_user",
                  "img_path", "img_shape",
                  "category", "title", "description",
                  "price", "is_selling", "created_date","log"]
        
        

        
        
        
        
        
        