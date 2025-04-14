# 👕 옷 색상 및 패턴 실시간 인식 프로그램
시각장애인을 위한 옷 색상 및 패턴 실시간 인식 프로그램입니다. 이 프로젝트는 시각장애인이 옷의 색상과 패턴을 인식하는 데 도움을 주기 위해 개발되었습니다.
<br>
<br>
<br>
# 🧠 프로젝트 개요
목표: 시각장애인이 옷의 색상과 패턴을 실시간으로 인식할 수 있도록 지원하는 프로그램 개발
<br>
<br>
<br>
## 기술 스택:
Python, OpenCV, 머신러닝 기반 색상 및 패턴 분석
<br>
<br>
<br>
## 주요 기능:
이미지에서 주요 색상 추출 및 분석
옷의 패턴 인식 (예: 스트라이프, 도트 등)
시각적 결과 출력 및 향후 음성 안내 기능 확장 가능성
<br>
<br>
<br>
# 📁 프로젝트 구조
Tell_me_Dominant_Colors.py: 주요 색상 추출 및 분석을 위한 핵심 스크립트<br>
DB.zip, Domi_Cols.zip, the_Last.zip: 데이터베이스 및 학습 모델 관련 파일<br>
result1.png ~ result4.png: 프로그램 실행 결과 예시 이미지<br>
READ_ME.txt: 프로젝트에 대한 추가 설명 파일
<br>
<br>
<br>
# 🚀 시작하기
### 레포지토리를 클론합니다:
git clone https://github.com/AlmightyDenver/Graduation-portfolio.git

### 필요한 패키지를 설치합니다:
pip install -r requirements.txt

### Tell_me_Dominant_Colors.py를 실행하여 주요 색상 추출 기능을 테스트합니다.

# 🖼️ 결과 예시
프로그램 실행 결과 예시 이미지는 다음과 같습니다:
![이미지 설명](result1.png)
![이미지 설명](result2.png)
![이미지 설명](result3.png)
![이미지 설명](result4.png)


# 📌 향후 개선 사항
다양한 패턴 인식 기능 추가
음성 안내 기능 통합
모바일 애플리케이션으로의 확장
<br>
<br>
<br>
# 졸논 최종s.zip 설명
1. DB
 - rgb.txt : color DB원본
 - RGB_REAL : gray  몇개 삭제, 중복 제거
 - RGB_REAL_KR : 한글패치


2. Domi_Cols
 - 3_Dominant_Color의 Photo ver., Webcam ver., Webcam_KR ver있음
=>코드에서 같이있는 RGB_REAL.txt, RGB_REAL_KR.txt 디렉토리 부분 수정해야함
=> Photo ver.은 사진 이미지 선택 방법 설명 3_Dominant_Color_Photo_ver_USAGE.txt참고


3. the_Last
 - Tell_me_Dominant_Colors.py : tensorflow object detection 폴더 안에있어야 실행가능. 마찬가지로 color DB 디렉토리 수정해야함
 - 실행 캡쳐본
