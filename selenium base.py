#pip3 install -U selenium
#pip3 install webdriver-manager
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.amazon.es/")

time.sleep(2)

#Search bar
#element = driver.find_element(By.XPATH,"/html/body/div[1]/span/form/div[2]/span[1]/span/input")
#element.click()

element = driver.find_element(By.XPATH,"/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[3]/div[1]/div/input")
element.send_keys("iphone 13")
element.send_keys(Keys.ENTER)
input()