from rest_framework import serializers

from user.models import User as UserModel

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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

# # TokenObtainPairSerializer를 상속하여 클레임 설정
# class SpartaTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
# 				# 생성된 토큰 가져오기
#         token = super().get_token(user)

#         # 사용자 지정 클레임 설정하기.
#         token['id'] = user.id
#         token['username'] = user.username

#         return token

