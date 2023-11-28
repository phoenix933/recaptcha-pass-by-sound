from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
from time import sleep
import os
from urllib.request import urlretrieve
import speech_recognition as sr
import soundfile
import sys

car_reg_number = sys.argv[1]
try:
    os.remove("captcha.wav")
except Exception:
    pass
try:
    os.remove("new.wav")
except Exception:
    pass
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
timeout_duration = 10  # Change the value (in seconds) as per your requirement
driver.set_page_load_timeout(timeout_duration)

try:
    driver.get("https://www.parkers.co.uk/car-specs/")
except TimeoutException:
    print("Page took too long to load!")
sleep(1)
try:
    driver.refresh()
except TimeoutException:
    print("Page took too long to load!")
sleep(1)
txt_vrm_lookup = driver.find_element(By.CSS_SELECTOR, "input.vrm-lookup__input")
txt_vrm_lookup.send_keys(car_reg_number)

txt_vrm_button = driver.find_element(
    By.CSS_SELECTOR, "button.vrm-lookup__button.button"
)
txt_vrm_button.click()

sleep(1)


driver.switch_to.default_content()
frame = driver.find_element(By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')
driver.switch_to.frame(frame)


driver.find_element(By.CSS_SELECTOR, "#rc-anchor-container").click()
sleep(2)
driver.switch_to.default_content()
frame = driver.find_element(
    By.CSS_SELECTOR, 'iframe[title="recaptcha challenge expires in two minutes"]'
)
driver.switch_to.frame(frame)

driver.find_element(By.CSS_SELECTOR, "#recaptcha-audio-button").click()
sleep(2)
src = driver.find_element(By.CSS_SELECTOR, "#audio-source").get_attribute("src")

file_path = os.path.join(os.getcwd(), "captcha.wav")
print(file_path)
urlretrieve(src, file_path)

data, samplerate = soundfile.read("captcha.wav")
soundfile.write("new.wav", data, samplerate, subtype="PCM_16")
r = sr.Recognizer()
with sr.AudioFile("new.wav") as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    # print(text)

driver.find_element(By.ID, "audio-response").send_keys(text)
try:
    driver.find_element(By.ID, "recaptcha-verify-button").click()
except TimeoutException:
    print("Page took too long to load!")


sleep(20)
# wait = WebDriverWait(driver, 15)
# link_url = wait.until(
#     EC.visibility_of_element_located((By.ID, "specs-confirmation-link"))
# )

link_url = driver.find_element(By.ID, "specs-confirmation-link").get_attribute("href")
print(link_url)
