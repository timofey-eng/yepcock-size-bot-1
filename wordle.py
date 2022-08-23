import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
import pyimgur
import os
from dotenv import load_dotenv


dictionary = open('dictionary.txt', 'r', encoding='utf-8').read().split('\n')
load_dotenv()
# IMGUR_ID
IMGUR_ID = os.getenv("IMGUR_ID")

#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")  # linux only
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage");
chrome_options.add_argument('--remote-debugging-port=9222')
#driver = webdriver.Chrome(executable_path=os.path.abspath(os.getcwd()) + '/chromedriver',options=chrome_options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
url = 'https://wordle.belousov.one/'
driver.get(url)
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div/div/div[1]/button').click()


def write_letter(letter):
    driver.find_element(By.CSS_SELECTOR, "[aria-label=" + letter).click()


def write_word(word):
    for i in range(5):
        write_letter(word[i])
    write_letter('ввод')


def write_clear():
    for _ in range(5):
        driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[2]/div[3]/button[1]').click()


dict1 = dictionary
letters = []
required = []
for i in range(5):
    letters.append([])
    for l in range(32):
        letters[i].append(chr(l + ord('а')))
print(letters)
count = 0
while True:
    dict2 = []
    while True:
        try:
            s = random.choice(dict1)
        except:
            s = 'проба'
        print(s)
        write_word(s)
        time.sleep(1)
        # soup = BeautifulSoup(driver.page_source, features='html.parser')
        # table = soup.findAll('div', class_='react-card-flip')
        # grip = table[0].div.div.div['class']
        table = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div/div/div/div[2]/div')
        grip = table[count * 5].get_attribute('class')
        if 'bg-correct' in grip or 'bg-present' in grip or 'bg-absent' in grip:
            break
        else:
            write_clear()
            dict1.remove(s)
    a = ''
    table = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div/div/div/div[2]/div')
    for i in range(5):
        grip = table[count * 5 + i]
        print(grip.text)
        if 'bg-correct' in grip.get_attribute('class'):
            a += '2'
        elif 'bg-present' in grip.get_attribute('class'):
            a += '1'
        else:
            a += '0'
    print(a)
    if a == '22222':
        print(s)
        time.sleep(2)
        image = 'wordle.png'
        screenshot_area = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div')
        with open(image, 'wb') as f:
            f.write(screenshot_area.screenshot_as_png)
        driver.close()
        im = pyimgur.Imgur(IMGUR_ID)
        uploaded_image = im.upload_image(image, title='wordle').link
        print(uploaded_image)
        with open('wordle_screenshot_imgur_link.txt', 'w') as f:
            f.write(uploaded_image)
        break
    for i in range(5):
        if a[i] == '2':
            if s[i] not in required:
                required.append(s[i])
            letters[i] = s[i]
    for i in range(5):
        if a[i] == '1':
            if s[i] not in required:
                required.append(s[i])
            if s[i] in letters[i]:
                letters[i].remove(s[i])
        if a[i] == '0':
            for l in range(5):
                if s[i] not in required:
                    if len(letters[l]) != 1:
                        if s[i] in letters[l]:
                            letters[l].remove(s[i])
    print(letters)
    for i in dict1:
        word = i
        b = True
        for l in range(5):
            try:
                if word[l] not in letters[l]:
                    b = False
            except:
                b = False
        for l in required:
            if l not in word:
                b = False
        if b:
            dict2.append(word)
    dict1 = dict2
    print(len(dict1))
    print(dict1)
    count += 1
    if count == 6:
        print(s)
        time.sleep(2)
        js_script = '''\
        arguments[0].style.display = 'none';
         '''
        word_hint = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[3]/p')
        driver.execute_script(js_script, word_hint)
        image = 'wordle.png'
        screenshot_area = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div')
        with open(image, 'wb') as f:
            f.write(screenshot_area.screenshot_as_png)
        driver.close()
        im = pyimgur.Imgur(IMGUR_ID)
        uploaded_image = im.upload_image(image, title='wordle').link
        print(uploaded_image)
        with open('wordle_not_solved_screenshot_imgur_link.txt', 'w') as f:
            f.write(uploaded_image)
        break
