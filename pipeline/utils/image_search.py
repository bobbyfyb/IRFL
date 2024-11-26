import json
import re
import time
import urllib.request

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from pipeline.assets.constants import image_formats
from pipeline.utils.image_details_db import ImageDetailsDB
from pipeline.utils.utils import get_str_hash, get_random_number, get_base64_format
from pipeline.assets.config import chromedriver_path

class ImageSearch:

    def __init__(self):
        self.image_metadata = []
        self.limit = 50
        self.img_detailes_saved = 0
        self.img_failed = 0
        self.img_exists = 0
        self.image_folder = ''
        self.website_url = ''
        self.google_url = "https://www.google.com/search?q={}&source=lnms&tbm=isch&hl=en&lr=lang_en"
        self.image_formats = image_formats
        self.scroll_interval = 5
        self.image_details_db = ImageDetailsDB()
        self.init_browser()

    def init_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        
        cService = webdriver.ChromeService(executable_path=chromedriver_path)
        # cService = webdriver.ChromeService(executable_path='/Users/artorias/Library/CloudStorage/OneDrive-筑波大学/projects/IRFL/pipeline/chromedriver-mac-arm64/chromedriver')
        cOptions = webdriver.ChromeOptions()
        # Add language preferences
        cOptions.add_argument("--lang=en-US")
        cOptions.add_argument("--accept-language=en-US")
        cOptions.add_argument("--disable-dev-shm-usage")
        cOptions.add_argument("--no-sandbox")
        cOptions.add_argument("--headless")
        
        self.browser = webdriver.Chrome(service=cService, options=cOptions)
        
        self.browser.set_window_size(1024, 768)
        self.browser.get('https://www.google.com/search?q=test&source=lnms&tbm=isch&hl=en&lr=lang_en')
        # self.change_region_and_activate_safe_search()

    def search(self, url):
        self.browser.get(url)
        time.sleep(2)
        element = self.browser.find_element(By.TAG_NAME, "body")
        for i in range(round(self.limit / 3.5)):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
        time.sleep(1)
        source = self.browser.page_source
        return source

    def change_region_and_activate_safe_search(self):
        # time.sleep(2)
        time.sleep(2)
        # self.browser.find_element(By.XPATH, '//div[@aria-label="Quick Settings"]').click()  # Opens settings
        self.browser.find_element(By.XPATH, '//div[@aria-label="Settings"]').click()  # Opens settings
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//a[text()='See all Search settings']").click()  # Click on See all settings time.sleep(1)
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//div[@id='ssc']").click()  # Toggle safe search
        self.browser.find_element(By.XPATH, "//a[@id='regionanchormore']").click()  # shows more regions
        self.browser.find_element(By.XPATH, "//div[@data-value='US']").click()  # Selecting US region
        self.browser.find_element(By.XPATH, "//div[@class='goog-inline-block jfk-button jfk-button-action']").click()  # Click on save button
        WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        self.browser.switch_to.alert.accept()

    def raise_error(self):
        raise ValueError('A very specific bad thing happened.')

    def get_img_format(self, link, response):
        for image_format in self.image_formats:
            if image_format in response.headers['content-type']:
                return image_format

        for image_format in self.image_formats:
            if '.' + image_format in link:
                return image_format
        return ''

    def save_image_details_by_base64(self, name, link, file_format):
        img_UUID = get_str_hash(link)
        self.image_details_db.put_item({'id': img_UUID, 'url': link, 'type': 'base64', 'label': name, 'websiteURL': self.website_url})
        self.image_metadata.append(img_UUID)
        return True

    def request_image_by_URL(self, link):
        response = None
        try:
            response = urllib.request.urlopen(urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'}), timeout=5)
        except:
            try:
                response = urllib.request.urlopen(urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'}), timeout=5)
            except:
                response = urllib.request.urlopen(urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'}), timeout=5)
        return response

    def save_image_details_by_URL(self, response, link, name):
        img_UUID = get_str_hash(link)
        img_format = self.get_img_format(link, response)
        if img_format == '':
            self.img_failed += 1
            return False
        self.image_details_db.put_item({'id': img_UUID, 'url': link, 'type': 'http', 'label': name, 'websiteURL': self.website_url})
        self.image_metadata.append(img_UUID)
        self.img_detailes_saved += 1
        return True
    
    def save_image_details_local(self, link, name, dir='/data2/fyb/figurative/idiom'):      
        response = self.request_image_by_URL(link)
        image_info = {}
        if response is not None:
            img_UUID = get_str_hash(link)
            img_format = self.get_img_format(link, response)
            if img_format == '':
                self.img_failed += 1
                return False
            if os.path.exists(f'{dir}/{img_UUID}.{img_format}'):
                self.img_exists += 1
                self.image_metadata.append(img_UUID)
                return
            with open(f'{dir}/{img_UUID}.{img_format}', 'wb') as f:
                f.write(response.read())
            
            image_info = {'id': img_UUID, 'url': link, 'type': 'http', 'label': name}
            with open(f'{dir}/searched_images.json', 'a') as f:
                f.write(json.dumps(image_info) + '\n')
            
            self.image_metadata.append(img_UUID)
            self.img_detailes_saved += 1
            return True


    def save_image_details(self, link, name, isBase64=False, file_format=''):
        imageUUID = get_str_hash(link)
        if self.image_details_db.has_item(imageUUID):
            self.img_exists += 1
            self.image_metadata.append(imageUUID)
            return

        if isBase64:
            return self.save_image_details_by_base64(name, link, file_format)
        else:
            response = self.request_image_by_URL(link)
            if response is not None:
                return self.save_image_details_by_URL(response, link, name)
        self.img_failed += 1
        return False

    def get_img_name(self, img):
        if img['alt'] is not None:
            img_description = re.sub(r'[^a-zA-Z0-9\s._-]', "", img.attrs['alt'])  # In .file name format
            return img_description[:400]
        return str(get_random_number(5))

    def save_image(self, image):
        image_name = image.attrs['alt']
        image_url = image.attrs['src']
        self.save_image_details_local(image_url, image_name)
        return True
        
    
    # def save_image(self, image):
    #     self.browser.find_element(By.XPATH, "//*[@data-id='{}']".format(image.attrs['data-id'])).click()
    #     time.sleep(4)
    #     image_details_panel = BeautifulSoup(str(self.browser.page_source), "html.parser")
    #     img_element = image_details_panel.find("div", class_="BIB1wf").find("img", {"jsname": "HiaYvf"})
    #     self.website_url = image_details_panel.find("div", class_="BIB1wf").find('a', class_='aDMkBb').attrs.get('href')
    #     base64_source, file_format = get_base64_format(img_element.attrs['src'])
    #     img_name = self.get_img_name(img_element)
    #     if base64_source is None:
    #         full_image_source_url = img_element.attrs['src']
    #         self.save_image_details(full_image_source_url, img_name)
    #         return True

    #     if base64_source is not None and file_format is not None:
    #         self.save_image_details(base64_source, img_name, True, file_format)
    #         return True

    #     self.img_failed += 1
    #     return False

    def iterate_over_image_results(self, soup):
                # Debug and find alternative containers
                print("Analyzing HTML structure...")
                
                # Try multiple possible selectors for images
                possible_containers = [
                    soup.find_all('div', class_='ivg-i'), # Common image result class
                    # soup.find_all('div', class_='rg_i'),  # Alternative image container
                    # soup.select('img[data-src]'),         # Images with data-src attribute
                    # soup.select('img[src]'),              # All images with src attribute
                ]
                
                image_results = []
                for container in possible_containers:
                    if container:
                        image_results = container
                        print(f"Found {len(container)} images")
                        break
                        
                if not image_results:
                    print("No images found in the HTML")
                    return
                
                self.img_detailes_saved = 0
                self.img_failed = 0
                self.img_exists = 0
                self.image_metadata = []
                
                for count, image in enumerate(image_results):
                    try:
                        if self.img_detailes_saved + self.img_exists >= self.limit:
                            break
                            
                        # Handle different HTML structures
                        if image.name == 'img':
                            img_element = image
                        else:
                            img_element = image.find('img')
                            
                        if img_element:
                            self.save_image(img_element)
                            
                    except Exception as e:
                        print(f"Error processing image {count}")
                        print(e)
                        self.img_failed += 1
            
                # Debug output
                print(f"Total images found: {len(image_results)}")  
    
    # def iterate_over_image_results(self, soup):
        
    #     with open("./soup.html", "w") as f:
    #         f.write(str(soup))
        
    #     image_results = list(list(soup.find('div', {"id": "islrg"}))[0].children)
            
    #     self.img_detailes_saved = 0
    #     self.img_failed = 0
    #     self.img_exists = 0
    #     self.image_metadata = []
    #     for count, image in enumerate(image_results):
    #         if image.name != 'div' or image.find('div', {"jscontroller": "hr4ghb"}) is not None:
    #             continue
    #         try:
    #             if self.img_detailes_saved + self.img_exists >= self.limit:
    #                 break
    #             self.save_image(image)

    #         except Exception as e:
    #             print(e)

    def google(self, query, limit):
        self.limit = limit
        source = self.search(self.google_url.format(query))
        soup = BeautifulSoup(str(source), "html.parser")
        self.iterate_over_image_results(soup)
        print('Query {}, with limit {}, saved {} images details successfully, {} images were already saved, fail to save {} images.'.format(query, limit, self.img_detailes_saved,
                                                                                                                                                  self.img_exists, self.img_failed))
        return self.img_detailes_saved, self.image_metadata
