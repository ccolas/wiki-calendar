#Import libraries (Don't change)
import sys
sys.path.append('/home/cedric/Documents/Perso/Scratch/Google-Image-Scraper')
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())
from google_scrapper import GoogleImageScraper
import os
# from patch import webdriver_executable


#Define file path (Don't change)
# webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
webdriver_path = '/usr/lib/chromium-browser/chromedriver'

#Parameters
headless = True
min_resolution=(0,0)
max_resolution=(1920,1080)

def get_google_image(query, save_directory, filename, shuffle_all=False, num_images=40):
    try:
        image_scrapper = GoogleImageScraper(webdriver_path, save_directory, query, num_images, headless, shuffle_all)
        image_scrapper.get_one_image(filename)
        return False
    except:
        return True
