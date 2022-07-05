from rest_framework import serializers

from user.models import User as UserModel

class UserSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        password = validated_data.pop("password", "")
        new_user = UserModel(**validated_data)
        new_user.set_password(password)
        new_user.save()
        return new_user
    
    class Meta:
        model =  UserModel
        fields = ["email", "password", "fullname", ]
        extra_kwargs = {
                  "password": {"write_only": True}
        }