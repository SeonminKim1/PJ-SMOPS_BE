from rest_framework import serializers

from art.models import Category as CategoryModel, Product, Article
from art.models import Product as ProductModel
from art.models import Log as LogModel
from art.models import ImageShape
        
from .models import Category, Product, ImageShape, Log

##################################################################
### Main Page
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["name"]

class ProductsMainSerializer(serializers.ModelSerializer):
    created_user = serializers.SerializerMethodField()
    def get_created_user(self, obj):
        return obj.created_user.fullname

    category = serializers.SerializerMethodField()
    def get_category(self,obj):
        return obj.category.name
    
    class Meta:
        model = Product
        fields = ["id", "category", "created_user", "img_path", "title", "description",
                  "price", "is_selling", "created_date"]

##################################################################
### Main Detail Page
class LogsSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    def get_product(self, obj):
        return obj.product.title

    old_owner = serializers.SerializerMethodField()
    def get_old_owner(self, obj):
        return obj.old_owner.fullname

    class Meta:
        model = Log
        fields = ['product', 'old_owner', 'updated_date', 'old_price']

class ProductsDeatilSerializer(serializers.ModelSerializer):
    created_user = serializers.SerializerMethodField()
    def get_created_user(self, obj):
        return obj.created_user.fullname
        
    category = serializers.SerializerMethodField()
    def get_category(self,obj):
        return obj.category.name

    owner_user = serializers.SerializerMethodField()
    def get_owner_user(self, obj):
        return obj.owner_user.fullname   

    img_shape = serializers.SerializerMethodField()
    def get_img_shape(self, obj):
        return obj.img_shape.shape   

    log = LogsSerializer(many=True, source="log_set")
    class Meta:
        model = Product
        fields = ["created_user", "owner_user",
                  "img_path", "img_shape",
                  "category", "title", "description",
                  "price", "is_selling", "created_date","log"]
        
        
# ==================

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"