from openai import OpenAI
import os
import dotenv
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#basic functions:
def click_buttons_by_id(driver, id):
  try:
    element = WebDriverWait(driver, 12).until(
    EC.presence_of_element_located((By.ID, id))
    )
    element.click()
  except selenium.common.exceptions.TimeoutException:
    print("button not found")
  except selenium.common.exceptions.ElementClickInterceptedException:
    print("Element click intercepted")
    
def click_buttons_by_class(driver, my_class):
  try:
    element = WebDriverWait(driver, 12).until(
    EC.presence_of_element_located((By.CLASS_NAME, my_class))
    )
    element.click()
  except selenium.common.exceptions.TimeoutException:
    print("button not found")

def click_button_by_testid(driver, testid):
  try:
    element = WebDriverWait(driver, 12).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{testid}"]'))
    )
    driver.execute_script("arguments[0].click();", element)
  except selenium.common.exceptions.TimeoutException:
    print("button not found")
    
def click_button_by_aria_label(driver, aria):
  try:
    element = WebDriverWait(driver, 12).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, f'[aria-label="{aria}"]'))
    )
    element.click()
  except selenium.common.exceptions.TimeoutException:
    print("button not found")

def send_text_to_button_by_id(driver, id, text):
  try:
    element = driver.find_element(By.ID, id)
    element.send_keys(text)
  except selenium.common.exceptions.TimeoutException:
    print("")

#complex functions:
def name_playlist(driver, text_field_id, save, playlist_name):
  try:
    element = WebDriverWait(driver, 12).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{text_field_id}"]'))
    )
    element.click()
    element.clear()
    element.send_keys(playlist_name)
    click_button_by_testid(driver, save)
  except selenium.common.exceptions.TimeoutException:
    print("button not found")

def add_song(driver, xpath, song, add):
  try:
    element = WebDriverWait(driver, 12).until(
    EC.presence_of_element_located((By.XPATH, xpath))
    )
    element.click()
    element.clear()
    element.send_keys(song)
    time.sleep(1.3)
    click_button_by_testid(driver, add)
  except selenium.common.exceptions.TimeoutException:
    print("button not found")

def login(driver):
  send_text_to_button_by_id(driver, 'login-username', text=os.getenv('USERNAME_SPOTIFY'))
  send_text_to_button_by_id(driver, 'login-password', text=os.getenv('PASSWORD_SPOTIFY'))
  time.sleep(0.3)
  click_buttons_by_id(driver, 'login-button')
  click_button_by_testid(driver, 'web-player-link')
  time.sleep(2)
  click_buttons_by_id(driver, 'onetrust-accept-btn-handler')
 
def create_playlist(driver, playlist_name):
  click_button_by_aria_label(driver, 'Create playlist or folder')
  click_buttons_by_class(driver, 'mWj8N7D_OlsbDgtQx5GW')
  click_buttons_by_class(driver, 'wCkmVGEQh3je1hrbsFBY')
  time.sleep(0.6)
  name_playlist(driver, 'playlist-edit-details-name-input', save='playlist-edit-details-save-button', playlist_name=playlist_name)
  
def create_list_of_songs(mood: str, artists: str):
  dotenv.load_dotenv()
  API_KEY = os.getenv('OPEN_AI_API_KEY')
  client = OpenAI(api_key=API_KEY)
  if not artists:
    artists = ''
    
  completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", 
           "content": """
           You are a music dj that knows a lot about a wide variety of genres and up and coming artists. 
           Your task will be to receive a mood or prompt from the user who will tell you what kind of music they want to hear and optionally a few artists as reference.
           Then, with this information your task is to only return a list of songs of size 15 and no additional text as follow. This is the most important task so make sure to do it correctly.
           Example: 'All too well (Taylor's version) - Taylor Swift, Song - Artist, song - Artist'
           If no artists are given as reference, it is up to you to choose the songs and artists that fit the mood, it is specially good in this case to use popular artists and songs.
           Adittionaly, since the list will be split using commas, make sure to avoid using them inside the names of the songs
           """},
          {
              "role": "user",
              "content": f"Build me a playlist based on the following mood: {mood} and use these artists as reference: {artists}"
          }
    ]
  ) 
  
  list_of_songs = completion.choices[0].message.content
  list_of_songs = list_of_songs.split(', ')
  
  completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", 
           "content": """
           You are a music dj that knows a lot about a wide variety of genres and up and coming artists. 
           Your task will be to receive a list of songs from various artists and from there, you will have to create a short and creative name for a playlist. 
           The more creative and in sync with the music you are given the better, you can use metaphors and other figures of speech to make the coolest name possible.
           Finally, when you return the name, make sure to only return the name you created and nothing else. If you can roast the user with the title, do so.
           example: Summery Vibes
           """},
          {
              "role": "user",
              "content": f"from the following list of songs {list_of_songs} give me a creative name for my playlist"
          }
    ]
  ) 
  
  my_playlist_name = completion.choices[0].message.content
  
  return list_of_songs, my_playlist_name


#Code that will automate the task:

#Load environment variables
dotenv.load_dotenv()
my_mood = input('What is your current mood?')
the_artists = input('Give me a few artists as a base :)')
#Call openai api to create the 
list_of_songs, my_playlist_name = create_list_of_songs(my_mood, artists=the_artists)
print(list_of_songs)

#start selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://accounts.spotify.com/en/login")
driver.maximize_window()
login(driver)
time.sleep(1)
create_playlist(driver, playlist_name=my_playlist_name)
time.sleep(0.5)
for song in list_of_songs:
  add_song(driver, '/html/body/div[5]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/main/section/div[2]/div[3]/div/section/div/div/input', song, 'add-to-playlist-button')
  time.sleep(0.3)
  
time.sleep(1)
#Start playing music
click_button_by_testid(driver, 'play-button')
input()