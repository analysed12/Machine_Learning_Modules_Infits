from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
import os
from selenium.webdriver.common.by import By
import wget
# import
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# Specify the chromedriver.exe path in your local system 
s= Service('C:/Users/Aman/Downloads/chromedriver.exe')
GOOGLE_CHROME_BIN = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
options = webdriver.ChromeOptions()
options.binary_location = GOOGLE_CHROME_BIN
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument('log-level=3')
driver = webdriver.Chrome(service=s,options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
print(driver.execute_script("return navigator.userAgent;"))
driver.implicitly_wait(10)
driver.set_window_size(1920, 1100)

start = time.time()
n_images = int(input("Enter the number of images you want to download:")) 
path = 'images/Datasets_ImageScrapping/'
Title = str(input("Enter the name of the food item: "))
newstr = Title.replace(" ", "+" )
google_urls = f"https://www.google.com/search?q={newstr}&tbm=isch&sa=X&ved=2ahUKEwjY8syuxv37AhWpRWwGHd4iAFcQ0pQJegQIDRAB&biw=1536&bih=714&dpr=1.25"
print(google_urls)

if not os.path.exists(path + Title):
  print(f'Making directory: {Title}')
  os.makedirs(path+Title)

driver.get(google_urls)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
var= 2 

# Change the directory as per your local machine 
os.chdir(f'D:/Learning/Ml Intern(analysed)/images/Datasets_ImageScrapping/{Title}')
while n_images != 0 :

# Specify the path that is in your local system 
  
  print(n_images)
  # print(var)
  try:
    driver.find_element(By.XPATH, f"//*[@id=\"islrg\"]/div[1]/div[{var}]/a[1]/div[1]/img").click()
    try:
      image = driver.find_element(By.XPATH, "//*[@class=\"n3VNCb KAlRDb\"]").get_attribute("src")
      wget.download(image)
    except:
      var+=1
      continue
  except:
    var+=1
    continue
      
  
  var += 1
  n_images -= 1
print()
print(f"The number of Images searched to get the result {var} ")
end = time.time()
print(f"{end - start} sec")
print()
print()
print("...................................")
print("All Images are Successfully downloaded!!")


