# Create your views here.
from rest_framework import viewsets, permissions, status, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from .models import User


# Test 용 CBV 입니다. endpoint : get_users/
class TestUserView(APIView):
    def get(self, request):
        users = User.objects.all()
        print(users)
        return Response({}, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = BookSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save() # create() 호출함.
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
