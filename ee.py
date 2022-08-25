from flask import Flask,render_template,redirect,request
import requests
from multiprocessing import Process
import time
import sen_all
from concurrent.futures import ThreadPoolExecutor
import RPi.GPIO as gp
import pandas as pd

# gardenAll 데이터 불러오기
plant_data = pd.read_csv("gardenAll.csv", encoding="euc-kr")

app = Flask(__name__)

# 1. 히터(18),팬(22),물펌프(23) GPIO 값 설정
gp.setwarnings(False)
gp.setmode(gp.BCM)
gp.setup(18,gp.OUT)
gp.setup(22,gp.OUT)
gp.setup(23,gp.OUT)

# 2. temp(온도), hd(습도), lux(조도), waterA(급수), waterD(배수), moi(토양습도) 센서값 띄어쓰기로 분리
# 아두이노에서 받은 센서값 계속 오라클db로 전달
# 반복 작업
def get_url(url):
    return requests.get(url)
data = sen_all.data_send()
temp, hd, lux, waterA, waterD, moi = data.split(' ')
def sensor_data(data):
    for i in range(10):
        data = sen_all.data_send()
        temp, hd, lux, waterA, waterD, moi = data.split(' ')
pro1 = Process(args=(data,), target=sensor_data)
pro1.start()      