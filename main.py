import time
import datetime

from selenium import webdriver
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import data.reply

# Firebase database 인증 및 앱 초기화
cred = credentials.Certificate("data/firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ndhs-covid19-survey-default-rtdb.firebaseio.com/'
})

dir_submit_date = db.reference('submit_date')  # 기본 위치 지정
dir_recent = db.reference('submit_date/recent_submit')
# dir_all_logs = db.reference('submit_date/all_submit_logs')

current_time = datetime.datetime.now()  # 2021-04-29 01:36:06.049279
str_current_time = str(current_time)
# print('현재 시간:', current_time)


autoSubmit = data.reply.autoSubmit  # 자동 제출 여부

last_date_str = dir_recent.get()

if last_date_str == "" or last_date_str is None:
    print("최종 제출시간을 찾을 수 없습니다.")
    last_date_str = "2000-01-01 00:00:00.000000"

last_date_obj = datetime.datetime.strptime(last_date_str, '%Y-%m-%d %H:%M:%S.%f')  # 2021-04-29 01:16:31.358402

current_date = current_time.strftime("%Y-%m-%d")  # 현재 날짜 (2021-04-29)
now_year = current_time.strftime("%Y")  # 현재 년도 (2021)
last_date = last_date_obj.strftime("%Y-%m-%d")  # 마지막 제출일(2021-04-28)

if current_date == last_date:  # 이미 제출함
    isReplied = True

else:  # 오늘 아직 제출 안함
    isReplied = False

if isReplied:
    goRun = False
    goWrite = False

    print("오늘은 설문을 이미 제출하였습니다. (최종 제출시각: " + last_date_str + ")")

else:

    while True:
        print("(최종 제출시각: " + last_date_str + ")")

        input_str = input("아직 설문을 제출하지 않으셨습니다. 지금 설문을 제출할까요? (Y/N) > ")
        input_str = input_str.lower().strip()

        if input_str == "y" or input_str == "yes" or input_str == "ㅛ" or input_str == "네":
            goRun = True
            goWrite = True
            driver = webdriver.Chrome(executable_path='./chromedriver_win32/chromedriver')
            break

        elif input_str == "n" or input_str == "no" or input_str == "ㅜ" or input_str == "아니오":
            goRun = False
            goWrite = False
            break

        elif input_str == "test":
            goRun = True
            goWrite = False
            autoSubmit = False  # 테스트모드에서는 자동제출 허용하지 않음.
            driver = webdriver.Chrome(executable_path='./chromedriver_win32/chromedriver')
            break


def AutoClose(t):
    print(str(t) + "초 후 자동으로 종료됩니다.")
    time.sleep(t)
    driver.close()


class AutoInput():
    def __init__(self, txt_Xpath, txt_target, input_Xpath, input_txt, autoSubmit):
        self.real_txt = driver.find_element_by_xpath(txt_Xpath).text  # 찾은 텍스트
        self._txt_target = txt_target  # 찾을 텍스트

        self.input_element = driver.find_element_by_xpath(input_Xpath)  # 자동으로 입력할 위치
        self._input_txt = input_txt  # 입력할 텍스트

        self._autoSubmit = autoSubmit

    def inputTEXT(self):

        if (self.real_txt == self._txt_target):
            print(self.real_txt)
            (self.input_element).send_keys(self._input_txt)
        else:
            print(self._txt_target + "를 찾지 못했습니다. (찾은 값: " + self.real_txt + ")")
            self._autoSubmit = False

        return self._autoSubmit

    def clickRadioBTN(self):

        if (self.real_txt == self._txt_target):
            print(self.real_txt)
            (self.input_element).click()

        else:
            print(self._txt_target + "를 찾지 못했습니다. (찾은 값: " + self.real_txt + ")")
            self._autoSubmit = False

        return self._autoSubmit


def AutoReply():
    driver.implicitly_wait(10)  # 10 seconds

    url_forms = data.reply.url
    autoClickBTN = data.reply.autoClickBTN

    googleFormsURL = url_forms

    driver.get(googleFormsURL)

    time.sleep(0.5)

    roomNum = AutoInput(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div',
        data.reply.txtHint,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input',
        data.reply.roomNum,
        autoSubmit
    )

    roomNum.inputTEXT()

    name = AutoInput(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div',
        data.reply.txtHint,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',
        data.reply.name,
        autoSubmit
    )

    name.inputTEXT()

    if (autoClickBTN):
        question1 = AutoInput(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/span/div/div[1]/label/div/div[2]/div/span',
            data.reply.question1,
            '//*[@id="i13"]/div[3]/div',
            '',
            autoSubmit
        )

        question1.clickRadioBTN()

        question2 = AutoInput(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div/span/div/div[1]/label/div/div[2]/div/span',
            data.reply.question2,
            '//*[@id="i23"]/div[3]/div',
            '',
            autoSubmit
        )

        question2.clickRadioBTN()

        question3 = AutoInput(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div[1]/div/label/div/div[2]/div/span',
            data.reply.question3,
            '//*[@id="i34"]/div[2]',
            '',
            autoSubmit
        )

        question3.clickRadioBTN()

    if (autoSubmit):
        print("3초 후 자동으로 제출됩니다.")
        time.sleep(3)
        subbitButton = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')
        subbitButton.click()
        print("제출이 완료되었습니다.")
        AutoClose(3)


    else:
        print("입력된 내용을 확인 후 직접 제출하세요.")


if goRun:
    AutoReply()
if goWrite:
    dir_submit_date.update({'recent_submit': str_current_time})

    dir_all_logs_year = db.reference('submit_date/all_submit_logs/{}'.format(now_year))
    dir_all_logs_year.push(str_current_time)

print("프로그램을 종료합니다.")
