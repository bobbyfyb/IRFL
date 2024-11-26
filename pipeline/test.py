from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.wait import WebDriverWait


chrome_options = Options()
chrome_options.add_argument("--headless")

cService = webdriver.ChromeService(executable_path="/Users/iiresearch/Library/CloudStorage/OneDrive-筑波大学/projects/IRFL/pipeline/chromedriver-mac-arm64/chromedriver")
cOptions = webdriver.ChromeOptions()
# Add language preferences
cOptions.add_argument("--lang=en-US")
cOptions.add_argument("--accept-language=en-US")
browser = webdriver.Chrome(service=cService, options=cOptions)

browser.set_window_size(1024, 768)
browser.get('https://www.google.com/search?q=test&source=lnms&tbm=isch&hl=en&lr=lang_en')

time.sleep(2)
        # self.browser.find_element(By.XPATH, '//div[@aria-label="Quick Settings"]').click()  # Opens settings
browser.find_element(By.XPATH, '//div[@aria-label="Settings"]').click()  # Opens settings
time.sleep(1)
browser.find_element(By.XPATH, "//a[text()='See all Search settings']").click()  # Click on See all settings time.sleep(1)
time.sleep(1)
browser.find_element(By.XPATH, "//div[@id='ssc']").click()  # Toggle safe search
browser.find_element(By.XPATH, "//a[@id='regionanchormore']").click()  # shows more regions
browser.find_element(By.XPATH, "//div[@data-value='US']").click()  # Selecting US region
browser.find_element(By.XPATH, "//div[@class='goog-inline-block jfk-button jfk-button-action']").click()  # Click on save button
WebDriverWait(browser, 10).until(EC.alert_is_present())
browser.switch_to.alert.accept()