import cv2
import time
import os
import threading
import numpy as np
import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates as denormalize_coordinates
import wave
import multiprocessing
import winsound
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import matplotlib.pyplot as plt 

counts=0


# 이메일 설정
def student(filep):

    email_sender = 'kim83290326@gmail.com'  # 발신자 이메일 주소
    email_receiver = 'wldnr5361@gmail.com'  # 수신자 이메일 주소
    email_subject = '학생이 졸고 있습니다'
    email_message = '안녕하세요! OOO학생이 졸고있습니다'

    # 이메일 구성
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = email_subject#.encode('utf-8)


    with open(filep, 'rb') as f:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename=filep)
        msg.attach(attachment)


    msg.attach(MIMEText(email_message, 'plain'))

    # SMTP 서버 연결
    smtp_server = 'smtp.gmail.com'  # Gmail SMTP 서버 주소
    smtp_port = 587  # Gmail SMTP 포트 번호
    sender_email = 'kim83290326@gmail.com'  # 발신자 이메일 주소
    sender_password = 'vqyx hqci olrr pzyq'  # 발신자 이메일 비밀번호

    # SMTP 서버 연결 및 이메일 보내기
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()
        print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print("이메일 전송 중 오류가 발생했습니다:", str(e))
        
# Mediapipe FaceMesh Solution Graph 객체를 초기화하는 함수
def get_mediapipe_app(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
):
    #  """Mediapipe FaceMesh Solution Graph 객체를 초기화하고 반환합니다"""
    face_mesh = mp.solutions.face_mesh.FaceMesh(
        max_num_faces=max_num_faces, # 감지할 최대 얼굴 수 
        refine_landmarks=refine_landmarks, #랜드마크 위치 더 정확하게 조절할지 여부
        min_detection_confidence=min_detection_confidence, # 최소 감지 신뢰도 임계값
        min_tracking_confidence=min_tracking_confidence, #최소 추적 신뢰도 임계값
    )

    return face_mesh

# 두 점 사이의 거리를 계산하는 함수
def distance(point_1, point_2):
   #유클리드 거리 계산
    dist = sum([(i - j) ** 2 for i, j in zip(point_1, point_2)]) ** 0.5
    return dist

#한 눈의 EAR(Eye Aspect Ratio)를 계산하는 함수
def get_ear(landmarks, refer_idxs, frame_width, frame_height):
    """
    Args-
        landmarks: (list) 감지된 랜드마크 목록
        refer_idxs: (list) 선택한 랜드마크의 인덱스 위치
                            P1, P2, P3, P4, P5, P6 순서대로
        frame_width: (int) 캡처된 프레임의 너비
        frame_height: (int) 캡처된 프레임의 높이
    Returns-
        ear: (float) 눈의 Eye Aspect Ratio
    """
    try:
         # 수평으로 두 점 사이의 유클리드 거리 계산
        coords_points = []
        for i in refer_idxs:
            lm = landmarks[i]
            coord = denormalize_coordinates(lm.x, lm.y, frame_width, frame_height)
            coords_points.append(coord)

         # 눈 landmark의 (x, y) 좌표
        P2_P6 = distance(coords_points[1], coords_points[5])
        P3_P5 = distance(coords_points[2], coords_points[4])
        P1_P4 = distance(coords_points[0], coords_points[3])

         # 눈의 Eye Aspect Ratio 계산
        ear = (P2_P6 + P3_P5) / (2.0 * P1_P4)

    except:
        ear = 0.0
        coords_points = None

    return ear, coords_points

# 양쪽 눈의 평균 EAR를 계산하는 함수
def calculate_avg_ear(landmarks, left_eye_idxs, right_eye_idxs, image_w, image_h):
    

    left_ear, left_lm_coordinates = get_ear(landmarks, left_eye_idxs, image_w, image_h)
    right_ear, right_lm_coordinates = get_ear(landmarks, right_eye_idxs, image_w, image_h)
    Avg_EAR = (left_ear + right_ear) / 2.0

    return Avg_EAR, (left_lm_coordinates, right_lm_coordinates)
#한쪽 눈과 양쪽 눈의 EAR를 따로 계산하는 것은 양쪽 눈이 서로 다른 상태에 있을 수 있기 때문일 수 있습니다. 
# 예를 들어, 사용자가 한 눈을 감았을 때, EAR은 해당 눈에 대해 더 작아질 것입니다. 
# 따라서, 두 눈의 EAR을 따로 계산하여 두 눈이 다른 상태에 있을 때도 각각의 눈을 독립적으로 판단하고 처리할 수 있습니다.

# 눈 랜드마크에 점을 그리는 함수
def plot_eye_landmarks(frame, left_lm_coordinates, right_lm_coordinates, color):
    frame.flags.writeable = True  # 프레임을 쓰기 가능하게 설정

    for lm_coordinates in [left_lm_coordinates, right_lm_coordinates]: #왼쪽눈과 오른쪽 눈의 랜드마크 순회 
        if lm_coordinates: # 해당 눈의 랜드마크 좌표가 있는경우 
            for coord in lm_coordinates: # 랜드마크부분에 동그라미
                cv2.circle(frame, coord, 2, color, -1) # 2- 반지름,-1=동그라미를 채울지말지

    frame = cv2.flip(frame, 1) #좌우반전
    return frame #랜드마크를 추가한 프레임을 반환합니다.

# 글자 입력부분 
def plot_text(image, text, origin, color, font=cv2.FONT_HERSHEY_SIMPLEX, fntScale=0.8, thickness=2):
    image = cv2.putText(image, text, origin, font, fntScale, color, thickness)
    return image


class VideoFrameHandler:
    def __init__(self):
        # 왼쪽,오른쪽 눈 랜드마크
        self.eye_idxs = {
            "left": [362, 385, 387, 263, 373, 380],
            "right": [33, 160, 158, 133, 153, 144],
        }

         # 랜드마크를 색칠하는 데 사용되는 값
        self.RED = (0, 0, 255)  # BGR
        self.GREEN = (0, 255, 0)  # BGR

         # Mediapipe FaceMesh 모델 초기화
        self.facemesh_model = get_mediapipe_app()

        # 상태 추적을 위한 변수들
        self.state_tracker = {
            "start_time": time.perf_counter(),
            "DROWSY_TIME": 0.0,  # EAR < EAR_THRESH인 동안 경과한 시간을 저장
            "COLOR": self.GREEN,
            "play_alarm": False,
        }
        self.play_obj = None
        self.EAR_txt_pos = (10, 30)
        self.playing = False
        self.drowsy_frame = None
        self.ear_values=[]
    def process(self, frame: np.array, thresholds: dict):
        
        '''졸음 감지 알고리즘을 구현하는 함수

        Args:
            frame: (np.array) 입력 프레임 매트릭스
            thresholds: (dict) EAR_THRESH와 WAIT_TIME의 두 가지 임계값을 포함하는 딕셔너리

        Returns:
            처리된 프레임과 알람을 울릴지 여부를 나타내는 부울 플래그 반환'''
        

        # 성능 향상을 위해 프레임을 쓰기 불가능하도록 표시
        frame.flags.writeable = False
        frame_h, frame_w, _ = frame.shape

        DROWSY_TIME_txt_pos = (430, 30) # 글자들 위치 
        ALM_txt_pos = (430, 60)

        results = self.facemesh_model.process(frame)
        # 얼굴을 감지하면
        if results.multi_face_landmarks:  
             #얼굴 랜드마크를 가져옴
            landmarks = results.multi_face_landmarks[0].landmark 
            # 눈의 EAR과 좌표를 계산합니다.
            EAR, coordinates = calculate_avg_ear(landmarks, self.eye_idxs["left"], self.eye_idxs["right"], frame_w, frame_h) 
            self.ear_values.append(EAR)
             # 랜드마크에 따라 눈을 표시합니다.
            frame = plot_eye_landmarks(frame, coordinates[0], coordinates[1], self.state_tracker["COLOR"])

            if EAR < thresholds["EAR_THRESH"]: #졸음 상태인경우

               # EAR이 임계값 미만인 동안 경과한 시간 증가
                # 그리고 다음 반복을 위해 start_time 재설정
                end_time = time.perf_counter() #현재시간 기록 

                self.state_tracker["DROWSY_TIME"] += end_time - self.state_tracker["start_time"] # EAR이 임계값 미만인 동안 경과한 시간 추가
                self.state_tracker["start_time"] = end_time # 다음 반복을 위해 start_time을 현재 시간으로 업데이트
                self.state_tracker["COLOR"] = self.RED     # 빨간색으로 표시 변경

                if self.state_tracker["DROWSY_TIME"] >= thresholds["WAIT_TIME"]:  # 설정한 졸음 경고 시간을 초과하면 알람 활성화
                    self.state_tracker["play_alarm"] = True
                    plot_text(frame, "WAKE UP!", ALM_txt_pos, self.state_tracker["COLOR"]) # 화면에 "WAKE UP!" 텍스트 표시

            else:
                 # 졸음 상태가 아닌 경우
                # 시작 시간과 졸음 시간 초기화
                self.state_tracker["start_time"] = time.perf_counter()
                self.state_tracker["DROWSY_TIME"] = 0.0
                self.state_tracker["COLOR"] = self.GREEN  # 초록색으로 표시 변경
                self.state_tracker["play_alarm"] = False  # 알람 비활성화

            # 현재 졸음 시간을 화면에 표시합니다.
            DROWSY_TIME_txt = f"SLEEP: {round(self.state_tracker['DROWSY_TIME'], 3)} sec" 

            plot_text(frame, DROWSY_TIME_txt, DROWSY_TIME_txt_pos, self.state_tracker["COLOR"])

        else: # 얼굴을 감지하지 못한 경우
            # 시작 시간과 졸음 시간을 초기화합니다.
            self.state_tracker["start_time"] = time.perf_counter()
            self.state_tracker["DROWSY_TIME"] = 0.0
            self.state_tracker["COLOR"] = self.GREEN  # 색상을 초록색으로 변경합니다.
            self.state_tracker["play_alarm"] = False  # 알람을 비활성화합니다.

            # Selfie-view 표시를 위해 프레임 수평으로 뒤집기
            frame = cv2.flip(frame, 1)

        

        return frame, self.state_tracker["play_alarm"]

def play_alarm():
    playing = False
    while True:
        if frame_handler.state_tracker["play_alarm"] and not playing:
            winsound.PlaySound(alarm_file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            playing = True
            global counts
            counts+=1
            
        elif not frame_handler.state_tracker["play_alarm"] and playing:
            winsound.PlaySound(None, winsound.SND_PURGE)
            playing = False
        time.sleep(0.1)  # 재생 상태를 주기적으로 확인

email_sent=False

def send_student_email(file_path): # 이메일 보내기 함수 
    global counts,email_sent
    if counts==2 and not email_sent:
        process=multiprocessing.Process(target=student, args=(file_path,))
        process.start()
        # student()

        email_sent=True
        counts=10
        return
def plot_ear(self):
    plt.plot(self.ear_values)
    plt.title('EAR Values')
    plt.xlabel('Frame')
    plt.ylabel('EAR')
    plt.show()

alarm_file_path = os.path.join("audio", "alarm.wav")

# 웹캠 캡처를 위한 VideoCapture 객체 생성    
cap = cv2.VideoCapture(0)  # 0은 기본 웹캠 사용하는 웹캠이 다른 경우 1, 2, ... 
cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# VideoFrameHandler 인스턴스 생성
frame_handler = VideoFrameHandler()
# 새로운 스레드에서 오디오 재생 함수 실행
alarm_thread = threading.Thread(target=play_alarm)
alarm_thread.daemon = True  # 주 스레드 종료 시 함께 종료되도록 데몬 설정
alarm_thread.start()
# 설정값 정의 (EAR_THRESH와 WAIT_TIME을 원하는 값으로 설정)
thresholds = {"EAR_THRESH": 0.2, "WAIT_TIME": 5.0}
check=0
# 웹캠 프레임을 처리
while True:
    ret, frame = cap.read()  # 프레임 읽기

    if not ret:
        break

    processed_frame, alarm = frame_handler.process(frame, thresholds)

    # 알람이 울려야 하는 경우
    if alarm:
        frame_handler.state_tracker["play_alarm"] = True
        cv2.imwrite('Smile.png',frame)
        send_student_email('Smile.png')
        # student_thread = threading.Thread(target=send_student_email)
        # student_thread.start() 
    
        # student_thread.join()
        # if frame_handler.state_tracker["play_alarm"] == True:
        #     if counts==2:
        #         student()
    else:
        #알람 X
        frame_handler.state_tracker["play_alarm"] = False
        almcnt=0
    cv2.imshow('Frame', processed_frame)  # 처리된 프레임을 화면에 출력
    cv2.setWindowProperty('Frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):  # 'q' 키를 누르면 종료
        break
    # frame_handler.play_obj = toggle_sound(frame_handler,key)
# 리소스 해제
cap.release()
cv2.destroyAllWindows()

plot_ear(frame_handler)