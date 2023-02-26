# TTS(Text To Speech) : 글자형 데이터를 소리로 바꿔주는 것
# STT(Speech To Text) : 소리형 데이터를 글자로 바꿔주는 것

# 가상환경 설정(터미널)

# windows : 
# python -m venv myenv -> 가상환경 만들기
# .\myenv\scripts\activate -> 가상환경 활성화

# mac :
# python3 -m venv myenv
# source myenv\bin\activate

# 패키지 설정(터미널)

# windows:
# pip install gTTS
# pip install playsound==1.2.2 (==1.2.2 버전 설정)

# mac :
# pip3 install gTTS
# pip3 install playsound
# pip3 install PyObjC

from gtts import gTTS # 클래스 불러오기

# 영어 작업
# text = 'Can I help you?' # 소리로 변환할 텍스트 적기
file_name = 'sample.mp3' # 파일이름 지정

# tts_en = gTTS(text=text, lang='en') # 텍스트 소리로 변환
# tts_en.save(file_name) # save 메소드를 통해서 저장

from playsound import playsound

# playsound(file_name) # 파일을 열지 않고 소스코드에서 바로 읽어줌

# 긴문장(파일에서 불러와서 처리)

# 파이썬에서는 파일을 열고 수정한 후, 닫는 형태의 프로세스가 많음
#  객체를 닫는 함수를 사용하지 않으면 프로그램이 종료되어도 계속 해당 객체가 열려있어 메모리를 점유
# open(), close() 메소드를 이용해 파일을 열고 닫을 수 있음
# with open -> close를 사용하지 않아도 구문 끝에서 객체를 닫음

#  #text 파일이 있는 경로
# path = r"C:\Users\Desktop\VS CODE"

# #text 파일 열기
# f = open(path+"/"+"test_data.txt", "r", encoding='utf-8') 

# #첫줄 읽어오기
# firstline = f.readline()

# #text 파일 닫기
# f.close()

# #첫줄 출력하기
# print(firstline)

with open('sample.txt', 'r', encoding='utf8') as f:
    text = f.read()

# 한글 작업
# text = '파이썬을 배우면 이런것도 할 수 있어요'
tts_ko = gTTS(text=text, lang='ko')
tts_ko.save(file_name) # save 메소드를 통해서 저장
playsound(file_name)