import threading
import multiprocessing
import time
import random
import os
# from app import database
import database

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, HardwareType, Popularity
from loguru import logger
from seleniumwire import webdriver
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException

logger.add('debug.log', format='{time} {level} {message}', compression='zip', 
            rotation='10 MB')
THREAD_COUNT = 5
BASE_DIR = Path(__file__).resolve().parent
DB_NAME = 'db.sqlite3'
DIR_DB = os.path.join(BASE_DIR.parent, DB_NAME)
NAME_DRIVER = 'geckodriver'
DIR_DRIVER = os.path.join(BASE_DIR, NAME_DRIVER)
software_names = [
    SoftwareName.CHROME.value, 
    SoftwareName.ANDROID.value, 
    SoftwareName.FIREFOX.value,
    SoftwareName.OPERA.value,
    ]

operating_systems = [
    OperatingSystem.WINDOWS.value,
    OperatingSystem.LINUX.value, 
    OperatingSystem.ANDROID.value, 
    OperatingSystem.UNIX.value,
    OperatingSystem.MAC.value,
    ]

hardware_types = [
    HardwareType.COMPUTER.value,
]

popularity = [
    Popularity.POPULAR.value,
]


class Prototipe:
    def __init__(self, target_url:str, proxy:str, name_video:str) -> None:
        self.proxy = proxy
        self.url = 'https://youtube.com'
        self.name_video = name_video
        self.target_url = f'/{target_url.split("/")[-1]}'
        user_agent_rotator = UserAgent(
            operating_systems=operating_systems, 
            software_names=software_names, 
            hardware_types=hardware_types, 
            popularity=popularity,
            limit=100
            )
        self.user_agent = user_agent_rotator.get_random_user_agent()
        self.ip, self.port, login, password = proxy.split(':')
        proxy_options = {
            'proxy': {
                'http': f'http://{login}:{password}@{self.ip}:{self.port}',
                'https': f'http://{login}:{password}@{self.ip}:{self.port}'
            }
        }
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.set_preference('general.useragent.override', self.user_agent)
        options.set_preference('dom.webdriver.enabled', False)
        self.driver = webdriver.Firefox(
            executable_path=DIR_DRIVER,
            seleniumwire_options=proxy_options,
            options=options
            )

    def check_exists_by_xpath(self, xpath:str):
        try:
            return self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return ''
    
    def check_css(self, css_selector:str):
        try:
            self.driver.find_element_by_css_selector(css_selector=css_selector)
            return True
        except NoSuchElementException:
            return False
        
    
    def go(self, time_low:int, time_max:int, id_:int):
        try:
            self.driver.get(url=self.url)
            time.sleep(random.randint(7,12))

            if self.check_css('ytd-button-renderer.ytd-consent-bump-v2-lightbox:nth-child(2) > a:nth-child(1) > tp-yt-paper-button:nth-child(1)'):
                button = self.driver.find_element_by_css_selector('ytd-button-renderer.ytd-consent-bump-v2-lightbox:nth-child(2) > a:nth-child(1) > tp-yt-paper-button:nth-child(1)')
                self.driver.execute_script('arguments[0].scrollIntoView();', button)
                button.click()
                time.sleep(random.randint(3,5))

            search = self.check_exists_by_xpath('//form[@id="search-form"]//div[@id="container"]//div[@id="search-input"]//input[@id="search"]')
            if search:
                for key in self.name_video:
                    search.send_keys(key)
                    time.sleep(random.uniform(0.05, 0.2))
                time.sleep(random.randint(3, 5))


                search_button = self.driver.find_element_by_xpath('//button[@id="search-icon-legacy"]')
                search_button.click()
                time.sleep(random.randint(3, 5))

                scroll_now = 0
                scroll_by = 25
                check = 0
                while self.check_exists_by_xpath(f'//a[@href="{self.target_url}"]') == '':
                    self.driver.execute_script(f'window.scrollBy({scroll_now}, {scroll_by});')
                    time.sleep(3)
                    scroll_by += 25
                    scroll_now += 25
                    check += 1
                    if check == 30:
                        logger.error('Timer scrolling == 30')
                        return False

                
                video = self.check_exists_by_xpath(f'//a[@href="{self.target_url}"]')
                if video:
                    video.click()
                time_view = random.randint(time_low, time_max)
                time.sleep(time_view)

                logger.info(f'{id_=} ::: {self.ip=}:{self.port} ---> {self.user_agent}')
                with database.sql(DIR_DB) as db:
                        db.update_count(int(db.video(id_)[6] + 1), id_)
                return True
            
        except Exception as ex:
            logger.error(ex)
            return False
        finally:
            self.driver.close()
            self.driver.quit()



def get_view(url, proxy, name, low, max_, id_, pool):
    with pool:
        view_video = Prototipe(target_url=url, proxy=proxy, name_video=name)
        view_video.go(time_low=low, time_max=max_, id_=id_)
            

def get_thread(video: list):
    NAME_PROCESS = multiprocessing.current_process().name
    POOL = threading.BoundedSemaphore(value=THREAD_COUNT)
    with database.sql(DIR_DB) as db:
        Proxy_list = db.get_proxy_avalible()
        while db.video(video[0])[6] < int(video[8]):
            proxy = random.choice(Proxy_list)[1]
            ThreadingVideo = threading.Thread(
                target=get_view,
                args=(
                    video[2],
                    proxy,
                    video[3],
                    int(video[4]),
                    int(video[5]),
                    int(video[0]), 
                    POOL,
                ),
                name=f'{NAME_PROCESS} {video[3]}',
            )
            ThreadingVideo.start()
            time.sleep(random.randint(1, 5))


def process() -> None:
    try:
        with database.sql(DIR_DB) as db:
            Video_list = db.get_videos()
        # for video in Video_list:
            # process = multiprocessing.Process(target=get_thread, args=(video,))
            # process.start()
        with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
            p.map(get_thread, Video_list)
    except Exception as ex:
        logger.error(ex)

def main():
    process()

if __name__ == '__main__':
    main()
