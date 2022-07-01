import io

import boto3
from service.cli import main

base_img_path = "../media/img/base.jpg"
style_img_path = ["../media/img/style.jpg"]
output_image = main(base_img_path, style_img_path)
print("===output_image", type(output_image))

in_mem_file = io.BytesIO()
print(in_mem_file, type(in_mem_file))
output_image.save(in_mem_file, "PNG")
in_mem_file.seek(0)

s3 = boto3.client("s3")
s3.put_object(
    ACL="public-read",
    Bucket="luckyseven-todaylunch",  # "{버킷이름}",
    Body=in_mem_file,  # 업로드할 파일 객체
    Key="output.png",  # S3에 업로드할 파일의 경로
    ContentType="image/png",  # 메타데이터 설정
)
print("끝===")
# Save the image to an in-memory file