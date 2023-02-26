# 음성인식모듈
# windows
# pip install speechrecognition

# 마이크를 통해서 인식되는 음성 인식
# pip install pyaudio

import speech_recognition as sr

# # import BeautifulSoup
# from bs4 import BeautifulSoup
# import requests

# BASE_URL = 'https://www.google.co.kr/'

# # get할 때 headers 인자를 이렇게 넣어주면 된다.
# requests.get(BASE_URL, headers={'User-Agent':'Mozilla/5.0'})

# SpeechRecognition에서 모든 작업들은 Recognizer 클래스에서 일어남
r = sr.Recognizer() # Recognizer 인스턴스 만들기

# 모두 사용하기 위해서는 API Key가 필요한데 google web speech API는 기본 API 키가 있어서 바로 사용할 수 있음

with sr.Microphone() as source: # 마이크로 들려오는 음성을 저장하려고
    print('듣고 있어요') # 약간시간이 걸릴 수 있어서 확인용 문장 추가
    audio = r.listen(source) # 마이크로부터 음성 듣기

# 예외처리
try:
    # 구글 api로 인식(하루 50회까지만 가능)
    # 영어
    # text = r.recognize_google(audio, language='en-US')
    # print(text)

    # 한국어
    text = r.recognize_google(audio, language='ko-KR')
    print(text)

except sr.UnknownValueError:
    print('인식실패') # 음성 인식 실패한 경우
except sr.RequestError as e:
    print('요청 실패 : {0}'.format(e)) # api key 오류, 네트워크 단절 등