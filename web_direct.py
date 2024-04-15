from selenium import webdriver
from selenium.webdriver.common.by import By
import keyboard 

class InfoScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
    
    def get_info(self, query):
        self.query = query
        self.driver.get("https://www.wikipedia.org")
        
        search_input = self.driver.find_element(By.XPATH,'//*[@id="searchInput"]')
        
        search_input.send_keys(query)
        
        search_button = self.driver.find_element(By.XPATH, '//*[@id="search-form"]/fieldset/button/i')
        search_button.click()
        
        print("Press 'Q' to exit the browser.")
        while True:
            if keyboard.is_pressed('q'):
                self.driver.quit() 
                print("Browser closed.")
                break
class MusicPlayer:
    def __init__(self):
        self.driver = webdriver.Chrome()
        
    def play_music(self, query):
        self.query = query
        self.driver.get("https://www.youtube.com/results?search_query=" + query)
        
        search_button = self.driver.find_element(By.XPATH, '//*[@id="title-wrapper"]')
        search_button.click()
        
        print("Press 'Q' to exit the browser.")
        while True:
            if keyboard.is_pressed('q'):
                self.driver.quit() 
                print("Browser closed.")
                break
            

