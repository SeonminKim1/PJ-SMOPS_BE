from rest_framework import serializers

from .models import Category, Product, ImageShape, Log
      
# Product : ['created_user', 'owner_user', 'img_path', 'img_shape', 'category', 'title', 'description', 'price', 'is_selling', 'created_date']
# Log : ['product', 'old_owner', 'updated_date', 'old_price']
# Category : ['name'] 

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


'''
class ProductsByCategorySerializer(serializers.ModelSerializer):
    created_user = serializers.SerializerMethodField()
    def get_created_user(self, obj):
        return obj.created_user.fullname

    category = serializers.SerializerMethodField()
    def get_category(self,obj):
        return obj.category.name
    
    log = LogsSerializer(many=True, source="log_set")
    
    class Meta:
        model = Product
        fields = ["created_user", "owner_user",
                  "img_path", "img_shape",
                  "category", "title", "description",
                  "price", "is_selling", "created_date","log"]
        category, created_user, img_path, title, description, price, is_selling, create_date
         # extra_kwargs = {
        #     'job_type': {
        #         'error_messages': {
        #             # required : 값이 입력되지 않았을 때 보여지는 메세지
        #             'required': '이메일을 입력해주세요.',
        #             # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
        #             'invalid': '알맞은 형식의 이메일을 입력해주세요.'
        #         },
        #         # required : validator에서 해당 값의 필요 여부를 판단한다.
        #         'required': False  # default : True
        #     },
        # }
'''