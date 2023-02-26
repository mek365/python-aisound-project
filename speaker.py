# 인공지능 스피커와 대화해보기
# 택스트애 특정 단어가 포함되게 말하면 반응하도록

# time -> 프로그램 중간에 중지되지 않게/ os -> 파일 삭제를 하기 위해
import time, os

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# SpeechRecognition에서 모든 작업들은 Recognizer 클래스에서 일어남
r = sr.Recognizer() # Recognizer 인스턴스 만들기
m = sr.Microphone() # 마이크를 통해 소리를 받을 객체 만들기

file_name = 'voice.mp3'

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
    else:
        answer_text = '다시 한 번 말씀해주시겠어요?'

    speak(answer_text)

# 컴퓨터가 소리내서 읽기(TTS)
def speak(text):
    print('[인공지능]' + text) # 인공지능과 나를 구분하기 위해 사용

    tts = gTTS(text=text, lang='ko')
    tts.save(file_name)
    playsound(file_name)

    if os.path.exists(file_name): # 파일 실행 후 지우기(파일이 남아있어 권한문제가 발생해서 사용)
        os.remove(file_name)
        # time.sleep(5) # 컴퓨터 성능이 떨어져서 지워지길 기다리기

# 먼저 컴퓨터가 한번 물어보고 시작
speak('무엇을 도와드릴까요?')

# os.remove(file_name)

# 어떤 목소리가 들리면 바로 그 처리할 수 있게 도와줌
stop_listening = r.listen_in_background(m, listen)

# 무한반복
while True:
    time.sleep(0.1)
# 모두 사용하기 위해서는 API Key가 필요한데 google web speech API는 기본 API 키가 있어서 바로 사용할 수 있음

# with sr.Microphone() as source: # 마이크로 들려오는 음성을 저장하려고
#     print('듣고 있어요') # 약간시간이 걸릴 수 있어서 확인용 문장 추가
#     audio = r.listen(source) # 마이크로부터 음성 듣기

# # 예외처리
# try:
#     # 구글 api로 인식(하루 50회까지만 가능)
#     # 영어
#     # text = r.recognize_google(audio, language='en-US')
#     # print(text)

#     # 한국어
#     text = r.recognize_google(audio, language='ko-KR')
#     print(text)

# except sr.UnknownValueError:
#     print('인식실패') # 음성 인식 실패한 경우
# except sr.RequestError as e:
#     print('요청 실패 : {0}'.format(e)) # api key 오류, 네트워크 단절 등