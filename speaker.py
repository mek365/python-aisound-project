# 인공지능 스피커와 대화해보기
# 택스트애 특정 단어가 포함되게 말하면 반응하도록

# https://kig2929kig.github.io/python%20project/aiSpeaker/ 로 업그레이드

# time -> 프로그램 중간에 중지되지 않게/ os -> 파일 삭제를 하기 위해
import time, os

from pathlib import Path
import requests
from bs4 import BeautifulSoup
import shutil

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# 음성인식(듣기, STT)
def listen(recognizer, audio):
    try:
        text = r.recognize_google(audio, language='ko')
        print('[사용자]' + text)
        answer(text)
        
    except sr.UnknownValueError:
        print('인식실패') # 음성 인식 실패한 경우
    except sr.RequestError as e:
        print('요청 실패 : {0}'.format(e)) # api key 오류, 네트워크 단절 등

def weather_info() :                                                                                                           
                                                                                                                               
    url_weather = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8' # 네이버 날씨  
    html = requests.get(url_weather)                                                                                           
    soup = BeautifulSoup(html.text, 'html.parser')                                                                             
                                                                                                                               
    #지역                                                                                                                      
    location = soup.find('div', {'class': 'title_area _area_panel'}).find('h2', 'title').text                                  
    #날씨 정보                                                                                                                 
    weather = soup.find('div', {'class': 'weather_info'})                                                                      
    #현재 온도                                                                                                                 
    temp = weather.find('div', {'class': 'temperature_text'}).text.strip()[5:-1]                                               
    #날씨 상태                                                                                                                 
    status = weather.find('span', {'class':'weather before_slash'}).text                                                       
    #체감                                                                                                                      
    term = weather.find('dl',  {'class':'summary_list'}).find('dd', {'class':'desc'})                                          
    term1 = term.text.strip()[:-1]                                                                                             
    #습도                                                                                                                      
    term2 = term.find_next('dd', {'class':'desc'}).text.strip()                                                                
    #미세먼지                                                                                                                  
    report = weather.find('ul',  {'today_chart_list'}).text.strip()                                                            
                                                                                                                               
    today = "오늘 {0} 날씨입니다. 현재 온도는 {1}도, 체감 온도는 {2}도, 습도 {3} 입니다.".format(location, temp, term1, term2) 
    today = today + report + "입니다. 오늘의 날씨 정보였습니다."                                                               
                                                                                                                               
    return today   

# 대답(분석해서 스피커가 어떤 대답을 할지)
def answer(input_text):
    answer_text = ''

    if '안녕' in input_text:
        answer_text = '안녕하세요? 반갑습니다.'
    elif '날씨' in input_text:
        answer_text = '오늘의 서울 기온은 20도 입니다. 맑은 하늘이 예상됩니다.'
    elif '환율' in input_text:
        answer_text = '원 달러 환율은 1380원입니다.'
    elif '고마워' in input_text:
        answer_text = '별말씀을요.'  
    elif '종료' in input_text:
        answer_text = '다음에 또 만나요.'   
        stop_listening(wait_for_stop=False)   # 어떤 시점이 되면 듣지 않게 하기
        print(stop_listening)
    else:
        answer_text = '다시 한 번 말씀해주시겠어요?'

    speak(answer_text)

# 컴퓨터가 소리내서 읽기(TTS)
def speak(text):
    print('[인공지능]' + text) # 인공지능과 나를 구분하기 위해 사용

    now_time = time.strftime('%Y%m%d%H%M%S')

    file_name = 'voice' + f'{now_time}' + '.mp3'
    # file_name = 'voice.mp3'
    # file_path = Path(r".\voice\\")
    file_path = r".\voice"

    tts = gTTS(text=text, lang='ko')
    tts.save(f'{file_path}\\{file_name}')
    playsound(f'{file_path}\\{file_name}')

    # if os.path.isfile(file_path): # 파일 실행 후 지우기(파일이 남아있어 권한문제가 발생해서 사용)
    #     print(os.path.isfile(file_path))
    #     file_path.unlink()      


file_path = r".\voice"

# 먼저 컴퓨터가 한번 물어보고 시작
speak('무엇을 도와드릴까요?')

# SpeechRecognition에서 모든 작업들은 Recognizer 클래스에서 일어남
r = sr.Recognizer() # Recognizer 인스턴스 만들기
m = sr.Microphone() # 마이크를 통해 소리를 받을 객체 만들기

# 어떤 목소리가 들리면 바로 그 처리할 수 있게 도와줌
stop_listening = r.listen_in_background(m, listen)
print(stop_listening)

if stop_listening == 'False':
    if os.path.exists(file_path):
        shutil.rmtree(file_path)

# 무한반복
while True:
    time.sleep(0.1)
