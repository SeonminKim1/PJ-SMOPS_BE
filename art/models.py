from django.db import models

from user.models import User


class Category(models.Model):
    # 인물, 정물, 배경, 동물
    name = models.CharField("카테고리", max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "CATEGORY"


class ImageShape(models.Model):
    shape = models.CharField("형태", max_length=10)

    class Meta:
        db_table = "IMAGESHAPE"


class Product(models.Model):
    created_user = models.ForeignKey(
        User,
        verbose_name="원작자",
        on_delete=models.CASCADE,
        related_name="product_create_user",
    )
    owner_user = models.ForeignKey(
        User,
        verbose_name="소유자",
        on_delete=models.CASCADE,
        related_name="product_owner_user",
    )
    img_path = models.FileField("작품경로", upload_to="media/img")

    img_shape = models.ForeignKey(
        ImageShape, verbose_name="작품형태", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, verbose_name="카테고리", on_delete=models.CASCADE
    )
    title = models.CharField("작품명", max_length=50)
    description = models.TextField("작품 설명", max_length=1000)
    price = models.IntegerField("가격")
    is_selling = models.BooleanField("판매중여부", default=False)
    created_date = models.DateTimeField("생성날짜", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "PRODUCT"


class Log(models.Model):
    # "updated_date에 old_owner 가 old_price원에 구매하였습니다."
    product = models.ForeignKey(Product, verbose_name="상품", on_delete=models.CASCADE)
    old_owner = models.ForeignKey(User, verbose_name="구매자", on_delete=models.CASCADE)
    updated_date = models.DateTimeField("구매 날짜", auto_now=True)
    old_price = models.IntegerField("낙찰가격")

    class Meta:
        db_table = "LOG"
