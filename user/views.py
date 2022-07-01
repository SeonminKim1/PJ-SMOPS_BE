from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from user.serializers import UserSerializer
from .models import User as UserModel

from rest_framework import permissions

# user/
class UserAPIView(APIView):
    # 로그인 한 유저 정보 출력
    def get(self, request):
        print(request.user)
        user = UserModel.objects.get(id=request.user.id)        
        
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
    # 회원가입
    def post(self, request):
        if not request.data["password"] == request.data["password_confirm"]:
            return Response({"errors": "비밀번호를 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"user" : serializer.data, "msg" : "회원가입 완료"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework_simplejwt.authentication import JWTAuthentication

# 인가된 사용자만 접근할 수 있는 View 생성
class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
		
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # Token에서 인증된 user만 가져온다.
        user = request.user
        print(f"user 정보 : {user}")
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Accepted"})