# 인공지능 스피커와 대화해보기
# 택스트애 특정 단어가 포함되게 말하면 반응하도록

# https://kig2929kig.github.io/python%20project/aiSpeaker/ 로 업그레이드

# time -> 프로그램 중간에 중지되지 않게/ os -> 파일 삭제를 하기 위해
import time, os

from pathlib import Path
import requests # HTTP 요청을 보낼 수 있도록 기능을 제공
from bs4 import BeautifulSoup # 웹 페이지의 정보를 쉽게 스크랩할 수 있도록 기능을 제공하는 라이브러리
import shutil

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

import feedparser
import re

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

# 날씨 정보
def weather_info() :                                                                                                           
                                                                                                                               
    url_weather = r"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8" # 네이버 날씨  
    html = requests.get(url_weather) # 데이터 요청
    # html.text 형태로 데이터를 받으면 지저분하게 데이터가 받아짐
    # BeautifulSoup을 사용해 데이터를 정리해서 받음                                                                                          
    soup = BeautifulSoup(html.text, 'html.parser')  # 응답받은 HTML 내용을 BeautifulSoup 클래스의 객체 형태로 생성/반환                                                                          
                                                                                                                               
    # 지역                                                                                                                      
    location = soup.find('div', {'class': 'title_area _area_panel'}).find('h2', 'title').text                                  
    # 날씨 정보                                                                                                                 
    weather = soup.find('div', {'class': 'weather_info'})                                                                      
    # 현재 온도                                                                                                                 
    temp = weather.find('div', {'class': 'temperature_text'}).text.strip()[5:-1]                                               
    # 날씨 상태                                                                                                                 
    status = weather.find('span', {'class':'weather before_slash'}).text                                                       
    # 체감                                                                                                                      
    term = weather.find('dl',  {'class':'summary_list'}).find('dd', {'class':'desc'})                                          
    term1 = term.text.strip()[:-1]                                                                                             
    # 습도                                                                                                                      
    term2 = term.find_next('dd', {'class':'desc'}).text.strip()                                                                
    # 미세먼지                                                                                                                  
    report = weather.find('ul',  {'today_chart_list'}).text.strip()                                                            
                                                                                                                               
    today = f'오늘 {location} 날씨입니다. 현재 온도는 {temp}도, 체감 온도는 {term1}도, 습도 {term2} 입니다.'
    today = today + report + "입니다. 오늘의 날씨 정보였습니다."                                                               
                                                                                                                               
    return today   

# 환율 정보
def exchange_rate_info() :                                                                                                           
                                                                                                                               
    url_exchange_rate = r"https://finance.naver.com/marketindex/" # 네이버 환율  
    html = requests.get(url_exchange_rate) # 데이터 요청                                                                                         
    soup = BeautifulSoup(html.text, 'html.parser')  # 응답받은 HTML 내용을 BeautifulSoup 클래스의 객체 형태로 생성/반환                                                                        
                                                                                                                               
    # 환율                                                                                                                      
    exchange_rate = soup.find('div', {'class': 'head_info point_up'}).find('span', 'value').text  

    # 증감 정보                                                                                                                
    exchange_rate_flow_num = soup.find('div', {'class': 'head_info point_up'}).find('span', 'change').text
    exchange_rate_flow_blind = soup.find('div', {'class': 'head_info point_up'}).find_all('span', 'blind')   
                                                                                                          
    exchange_rate_flow_blind_text = re.sub(r"[^ㄱ-ㅣ가-힣\s]", "", str(exchange_rate_flow_blind[1])) # 정규식을 이용해 한글만 추출                                                                                                                      
    today_exchange_rate = f'오늘 원달러 환율 정보는 {exchange_rate} 원입니다. 전일 대비 {exchange_rate_flow_num} {exchange_rate_flow_blind_text}했습니다.'                                                              
                                                                                                                               
    return today_exchange_rate   

# RSS - google news feed
# Rich Site Summary : 새 기사들의 제목만, 또는 새 기사들 전체를 뽑아서 하나의 파일로 만들어 둔 것
def news_info() :                                               
    url = r"https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko" 
    news_data = []                                            
    news_rss = feedparser.parse(url) # 파싱                  
    for title in news_rss.entries :  # 엔트리에 딕셔너리 형태로 데이터가 담겨져 있음                         
        news_data.append(title.title) 

    today_news = f'오늘 주요 뉴스 3개를 알려드릴게요. {news_data[0:3]}. 이상입니다.'                                                   
    return today_news  

# 대답(분석해서 스피커가 어떤 대답을 할지)
def answer(input_text):
    answer_text = ''

    if '안녕' in input_text:
        answer_text = '안녕하세요? 반갑습니다.'
    elif '날씨' in input_text:
        answer_text = weather_info()
    elif '환율' in input_text:
        answer_text = exchange_rate_info()
    elif '뉴스' in input_text:
        answer_text = news_info() 
    elif '고마워' in input_text:
        answer_text = '별말씀을요.'  
    elif '종료' in input_text:
        answer_text = '다음에 또 만나요.'   
        stop_listening = 'X'   # 어떤 시점이 되면 듣지 않게 하기
    else:
        answer_text = '다시 한 번 말씀해주시겠어요?'

    speak(answer_text)
    return stop_listening

# 컴퓨터가 소리내서 읽기(TTS)
def speak(text):
    print('[인공지능]' + text) # 인공지능과 나를 구분하기 위해 사용

    now_time = time.strftime('%Y%m%d%H%M%S')

    file_name = 'voice' + f'{now_time}' + '.mp3'
    # file_name = 'voice.mp3'
    # file_name = 'voice.mp3'
    # file_path = Path(r".\voice\\")
    file_path = r".\voice"

    tts = gTTS(text=text, lang='ko')
    tts.save(f'{file_path}\\{file_name}')
    playsound(f'{file_path}\\{file_name}')

    # if os.path.isfile(f'{file_path}\\{file_name}'): # 파일 실행 후 지우기(파일이 남아있어 권한문제가 발생해서 사용)
        
    #     os.remove(f'{file_path}\\{file_name}')
        # file_path.unlink()      


file_path = r".\voice"

# 먼저 컴퓨터가 한번 물어보고 시작
speak('무엇을 도와드릴까요?')

# SpeechRecognition에서 모든 작업들은 Recognizer 클래스에서 일어남
r = sr.Recognizer() # Recognizer 인스턴스 만들기
m = sr.Microphone() # 마이크를 통해 소리를 받을 객체 만들기

# 어떤 목소리가 들리면 바로 그 처리할 수 있게 도와줌
stop_listening = r.listen_in_background(m, listen)

if stop_listening == False:
    if os.path.exists(file_path):
        shutil.rmtree(file_path)

# 무한반복
while stop_listening != False:
    time.sleep(0.1)
