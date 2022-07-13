from email.headerregistry import ContentDispositionHeader
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

# Create your tests here.

# 이미지업로드(임시 파일을 만들어 가상 이미지 생성)
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile # 임시파일을 만드는 라이브러리

def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file
    

class ArticleCreateTest(APITestCase):
    # 테스트를 시작할 때 모든 메서드에 대해서 아래 함수 실행됨
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "ggg@ggg.com","fullname": "GGG", "password": "ggg"}
        cls.article_data = {"title": "some title", "content": "some content"}
        cls.user = User.objects.create_user('ggg@ggg.com', 'ggg')
    
    
    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
    
    # 테스트 함수 명은 반드시 맨앞에 test_ 가 붙어있어야한다!
    # 로그인이 되어있지 않은 유저가 게시글 작성 시도 시 401
    def test_fail_if_not_logged_in(self):
        url = reverse("article_view")
        response = self.client.post(url, self.article_data)
        self.assertEqual(response.status_code, 401)
            
    # 글작성 테스트(이미지 없음)
    def test_create_article(self):
        response = self.client.post(
            path=reverse("article_view"),
            data=self.article_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.data["message"], "글 작성 완료!")
        self.assertEqual(response.status_code, 200)
        
    # 글작성 테스트(이미지 포함)
    def test_create_article_with_image(self):
        # 임시 이미지 파일 생성
        temp_file = tempfile.NamedTemporaryFile() # 이름이있는 그냥 빈파일 생성
        temp_file.name = "image.png"  # 이름 지정
        image_file = get_temporary_image(temp_file) # 빈파일을 아까 만들어둔 함수에 인자로 줘서 이미지 파일로 생성
        image_file.seek(0) # 첫번째 프레임을 가져와야함
        
        # 생성한 이미지 파일을 article_data에 추가
        self.article_data["image"] = image_file
        
        # 전송
        response = self.client.post(
            path=reverse("article_view"),
            data=encode_multipart(data=self.article_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.data["message"], "글 작성 완료!")
        self.assertEqual(response.status_code, 200)