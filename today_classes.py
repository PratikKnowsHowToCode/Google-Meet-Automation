import calendar
from datetime import datetime
import webbrowser
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pyautogui as pag

opt = Options()
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})

# WHEN THESE WORDS ARE TRIGGERED A MESSAGE WILL BE SENT
alertWords = ["your_name", "are you there", "unmute yourself", "say something", "can you hear me"]

# TIME TABLE HERE
subjects = {
    'monday': ['UNIX', 'OOAD', 'CD', 'OS', 'DBMS'],
    'tuesday': ['CY', 'AI', 'MMA', 'DS', 'OS'],
    'friday': ['OOAD', 'PEHV', 'CD', 'OS', 'UNIX'],
}

# GOOGLE MEET LINKS TO RESPECTIVE SUBJECTS
classes = {
    'UNIX': 'https://meet.google.com/dux-eoqu-tsz',
    'CD': 'http://meet.google.com/uif-bfcq-bat',
    'PEHV': 'link_to_sub',
    'OS': 'link_to_sub',
    'OOAD': 'link_to_sub',
    'DBMS': 'link_to_sub'
}

# RETURNS CURRENT DAY
def find_day():
    date_and_time = datetime.now()
    date = str(date_and_time.day) + ' ' + str(date_and_time.month) + ' ' + str(date_and_time.year)
    date = datetime.strptime(date, '%d %m %Y').weekday()
    day = calendar.day_name[date]
    return day.lower()

# RETURNS CURRENT DATE CLASSES
def find_classes():
    subs = []
    day = find_day()
    classes_today = subjects.get(day, [])
    if day not in ['wednesday', 'thursday', 'saturday', 'sunday']:
        timings = ['09:30 am - 10:40 am', '10:50 am - 11:30 am', '11:40 pm - 12:20 pm', '12:30 am - 01:10 pm', '02:10 pm - 02:50 pm']
        for i in range(len(timings)):
            formatted = '{} {}'.format(timings[i], classes_today[i])
            subs.append(formatted)
    return subs

def classes_today():
    subs = find_classes()
    for i in subs:
        time_now = datetime.now().time()
        time_str = str(time_now).split(":")
        if time_str[0] == i[0:2] and time_str[1] >= i[3:5]:
            print('\n\t' + i, '<-- Present Session')
        elif time_str[0] == i[11:13] and time_str[1] < i[14:16]:
            print('\n\t' + i, '<-- Present Session')
        else:
            print('\n\t' + i)

def open_link(url):
    try:
        driver = webdriver.Chrome(options=opt, executable_path='C:\\Program Files (x86)\\chromedriver.exe')
        driver.get('https://accounts.google.com/ServiceLogin/identifier?service=classroom&passive=1209600&continue=https%3A%2F%2Fclassroom.google.com%2F&followup=https%3A%2F%2Fclassroom.google.com%2F&emr=1&flowName=GlifWebSignIn&flowEntry=AddSession')

        # Logs in the classroom
        username = driver.find_element_by_id('identifierId')
        username.click()
        username.send_keys('pratikkumar20062004@gmail.com')

        next = driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button/div[2]')
        next.click()
        time.sleep(2)

        password = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        password.click()
        password.send_keys('Triple_H-2022')

        next = driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button/div[2]')
        next.click()
        time.sleep(15)

        driver.get(url)
        time.sleep(7)

        # turns off camera
        camera = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[2]/div/div')
        camera.click()

        # turns off mic
        mic = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[1]/div/div/div')
        mic.click()

        # clicks join button
        join = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]')
        join.click()
        time.sleep(3)

        # closes the popup
        driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[2]/div[3]/div').click()
        time.sleep(3)

        # turn on captions
        driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[8]/div[3]/div[9]/div[3]/div[2]/div/span/span/div').click()
        time.sleep(5)

        # Reads the text from captions
        while True:
            try:
                elems = driver.find_element_by_class_name("VbkSUe")
                captioTextLower = str(elems.text).lower()
                for word in alertWords:
                    if word in captioTextLower:
                        driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[8]/div[3]/div[6]/div[3]/div/div[2]/div[3]').click()
                        time.sleep(2)
                        pag.write("Yes sir ! I'm Present ! Mic issue 😥", interval=0.1)
                        time.sleep(0.5)
                        pag.press('enter')
                        time.sleep(2)
                time.sleep(0.5)
            except (NoSuchElementException, StaleElementReferenceException):
                time.sleep(1)
    except:
        time.sleep(3)
