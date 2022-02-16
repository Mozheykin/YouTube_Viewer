from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
import time
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import random

#Wedriver - https://github.com/mozilla/geckodriver/releases
#thereading - https://www.youtube.com/watch?v=R4P7BSFH_oE

name_driver = 'geckodriver'

software_names = [SoftwareName.CHROME.value, SoftwareName.ANDROID.value, SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.ANDROID.value]



id = 'search'

class prototipe:
    def __init__(self, target_url:str, proxy:str, name_video:str) -> None:
        self.proxy = proxy
        self.url = 'https://youtube.com'
        self.name_video = name_video
        self.target_url = f'/{target_url.split("/")[-1]}'
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        ip, port, login, password = proxy.split(':')
        proxy_options = {
            'proxy': {
                'https': f'http://{login}:{password}@{ip}:{port}'
            }
        }
        options = webdriver.FirefoxOptions()
        options.set_preference('general.useragent.override', user_agent)
        options.set_preference('dom.webdriver.enabled', False)
        self.driver = webdriver.Firefox(executable_path=os.path.join(os.getcwd(), name_driver), seleniumwire_options=proxy_options)

    def check_exists_by_xpath(self, xpath:str):
        try:
            return self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return ''
        
    
    def go(self, time_low:int, time_max:int):
        try:
            self.driver.get(url=self.url)
            time.sleep(5)

            button = self.driver.find_element_by_css_selector('ytd-button-renderer.ytd-consent-bump-v2-lightbox:nth-child(2) > a:nth-child(1) > tp-yt-paper-button:nth-child(1)')
            self.driver.execute_script('arguments[0].scrollIntoView();', button)
            button.click()
            time.sleep(random.randint(3,5))


            search = self.check_exists_by_xpath("//input[@id='search']").send_keys(self.name_video)
            time.sleep(random.randint(2,3))   

            search_button = self.check_exists_by_xpath("//button[@id='search-icon-legacy']").click()
            time.sleep(random.randint(1,5))

            scroll_now = 0
            scroll_by = 25
            while self.check_exists_by_xpath(f'//a[@href="{self.target_url}"]') == '':
                self.driver.execute_script(f'window.scrollBy({scroll_now}, {scroll_by});')
                time.sleep(3)
                scroll_by += 25
                scroll_now += 25
            
            video = self.check_exists_by_xpath(f'//a[@href="{self.target_url}"]').click()
            time.sleep(random.randint(time_low, time_max))
            
        except Exception as ex:
            print(ex)
        finally:
            self.driver.close()
            self.driver.quit()
