import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.youtube.com/watch?v=xvFZjo5PgG0")


""" element = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[2]/div")
element.click()

#Search bar
element = driver.find_element(By.XPATH,"/html/body/div[1]/span/form/div[2]/span[1]/span/input")
element.click()
 """

input()