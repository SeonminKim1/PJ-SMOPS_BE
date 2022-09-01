![image](https://user-images.githubusercontent.com/33525798/177453882-a8d55a06-1556-4a63-b1f8-244fca57b0a4.png)

## :owl: SMOPS (Selling My Oil Paintings Service)
- 나만의 유화를 만들어 판매하거나 구매할 수 있는 웹 서비스

## :panda_face: Introduction
- **주제** : 유화 제작 및 판매 사이트 
- **기간** : 2022.06.28 (화) ~ 2022.07.06 (수)
- **Team** : 김선민 ([Github](https://github.com/SeonminKim1)), 김민기 ([Github](https://github.com/kmingky)), 박재현 ([Github](https://github.com/Aeius)), 황신혜 ([Github](https://github.com/hwangshinhye)) 

<hr>

## 📚 Project Structure
![image](https://user-images.githubusercontent.com/33525798/177453424-fbabf1d3-6109-4e68-a9cd-83c265fc4637.png)
<hr>

## :handshake: Project-Rules
#### Scheduling & API 
- [Git Project Link](https://github.com/SeonminKim1/SMOPS-BE/projects/1) / [간트차트 Link](https://docs.google.com/spreadsheets/d/1_1Sx46dnKnI8_DLJQzAASMSr7u525RFjm2Iat0beU14/edit#gid=375979933) / [API Design Link](https://www.notion.so/12cc32feafcb4e81b2377f07b04a6824?v=5b05b526a18e434cb44d62f044b26bf7)
- [Git BE Issue Link](https://github.com/SeonminKim1/SMOPS-BE/issues) / [Git FE Issue Link](https://github.com/SeonminKim1/SMOPS-FE/issues)

#### Branch Info
- main : LocalHost 실행 branch
- publish : EC2 Hosting 실행 Branch

#### Repository Info
- [SMOPS-FE Project](https://github.com/SeonminKim1/SMOPS-FE)

#### Figma Mock-up
![image](https://user-images.githubusercontent.com/33525798/177453735-59c483e0-a638-42fd-bccb-47b1795641a3.png)

#### DB Modeling   
![image](https://user-images.githubusercontent.com/33525798/177455609-da9e00a8-560e-45d2-a174-b300e86b18c6.png)

<hr>

## 👉 Getting-Started

``` Run
## FrontEnd Settings
$ git clone https://github.com/SeonminKim1/SMOPS-FE
$ cd SMOPS-FE/
- Install vscode extensions : Live Server 
- Run Live Server

## Backend Settings
$ git clone https://github.com/SeonminKim1/SMOPS-BE
$ cd SMOPS-BE/
$ pip install -r requirements.txt

- Make 'my_settings.py' from 'ex_my_settings.py
$ python manage.py makemigrations
$ python manage.py migrations
$ python manage.py runserver

# if you apply code convention by black & isort
$ python auto_cleancode.py
```

<hr>

## 👉 Structure
```
┌─smops
├── smops               // project
│   ├── urls.py       
│   ├── settings.py     // setting
│   └── ...
├── art                 // app
│   ├── models.py       // DB Model - User
│   ├── views.py        // View Functions
│   ├── serializers.py  // Serializers
│   └── ...
├── mygallery           // app
│   ├── models.py       // DB Model - Restaurant, Category
│   ├── views.py        // View Functions
│   ├── serializers.py  // Serializers
│   └── ...
├── ai                  // app + ai GAN
│   ├── service/        // AI Style Transfer 
│   ├── models.py       // DB Model - Star 
│   ├── views.py        // View Functions
│   ├── upload.py       // AWS S3 Upload Code 
│   ├── serializers.py  // Serializers
│   └── ...
├── user                // app
│   ├── models.py       // DB Model - Diary
│   ├── views.py        // View Functions
│   ├── serializers.py  // Serializers
│   └── ...
├── media 
│   └── test_img/       // test img    
│
├── **manage.py**           // 메인
└── requirements.txt
```

<hr>


## :computer: Development

#### 👉 Login/Join Page
- 회원가입 vaildation
- 로그인 JWT Token 부여
- ![image](https://user-images.githubusercontent.com/33525798/177491113-4c7bfeba-a06b-4318-8284-645b2d04ffa4.png)


#### 👉 유화 메인 페이지
- 유화 카테고리 별 조회 : 인물화, 풍경화, 정물화, 동물화
- 유화 필터링 별 조회
   - (1) 정렬 : 등록일, 가격 등
   - (2) 가격 범위 : ~10만원, ~30만원
   - (3) 그림형태
- 유화 아티스트 검색
![image](https://user-images.githubusercontent.com/33525798/177491092-a2c4d2d8-fec9-46ad-bb43-9db7761b5c94.png)


#### 👉 유화 상세 페이지
- 유화 정보 조회
- 유화 로그 조회 (히스토리)
- 유화 구매 하기
- 시연 화면
![image](https://user-images.githubusercontent.com/33525798/177491675-803cad93-8ec6-470e-90aa-61da4d945b94.png)


#### 마이 갤러리 페이지
- 보유 중인 내 유화 조회
- 유화 판매 상태로 업데이트 / 삭제
- 유화 로그 조회 (히스토리)
- 시연 화면
![image](https://user-images.githubusercontent.com/33525798/177492835-9ad05cae-e962-4795-ac32-a4a225aa4836.png)


#### 유화 만들기 페이지 (AI)
- Base 이미지, Style 이미지 업로드
- StyleGAN 모델 학습 (RUN 버튼)
- 학습 결과 내 유화로 등록
- 시연 화면
![image](https://user-images.githubusercontent.com/33525798/177491166-fcc523d5-d761-4d6f-9bf1-55dc5188695a.png)


#### AWS Infra
- AWS EC2 이용한 외부 Publish 배포
- AWS S3 User 이미지 업로드 및 정적 파일 관리 
- AWS IAM 부여하여 Infra Team 공동 관리

<hr>

## 🛡 Trouble Shooting
#### ⚡ 문제 발생 
- 각자 파트를 나눠서 작업을 하던 도중, 유화제작 담당과 백엔드 담당이 함께 작업을 해야하는 부분이 생김
#### ⚡ 문제 원인
- 프론트 단에서 이미지를 선택한 뒤 두 이미지를 통해 유화제작을 시키고 난 뒤 제작된 유화를 다시 프론트단에서 미리보기와 동시에 가지고 있다가    
최종 유화 등록 시 해당 제작된 유화의 이미지파일을 S3에 등록하고 URL를 리턴 받아 입력한 유화의 제목, URL을 DB에 저장하는 과정에 있어    
서로의 파트가 나눠져있기 때문에 의사소통이 필요한 상황
#### ⚡ 문제 해결
- 서로 각자 작업분에 대해서 설명하는 것도 좋지만 프로젝트를 짧은기간 동안 보다 효율적으로 운영하기 위해 아예 VSCode의 Extension인 Live Share를 이용하여 실시간으로 같이 코딩을 해가면서 데이터의 흐름이나 코드들에 대한 이해도 하며 빠르게 피드백과 동시에 코드를 작성하여 보다 원할하게 작업을 진행 할 수 있었습니다.

