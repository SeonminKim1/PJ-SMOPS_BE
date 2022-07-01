from rest_framework import serializers

from user.models import User as UserModel


class UserSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    class Meta:
        model =  UserModel
        fields = ["email", "password", "fullname", ]
        
        
        
