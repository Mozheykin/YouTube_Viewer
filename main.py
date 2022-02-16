from distutils import command
import prototipe
import threading
import time
import random
import argparse
from termcolor import colored
import database


target_url = 'https://www.youtube.com/watch?v=gHZ73tQ9XAU'
name_video = 'How to Grow a Mechanic Shop Business with Digital Marketing Strategy'
THREAD_COUNT = 5
NAME_DB = 'sqlite.db'


# target_url1 = 'https://www.youtube.com/watch?v=0JJTdpKwA28'
# name_video1 = 'Meditation Vibes Sounds & Ambience for Relaxation, Sleep, Study and Meditation | Get Some Sleep'
# target_url2 = 'https://www.youtube.com/watch?v=nSfU5_hpWbo'
# name_video2 = 'Hello Kitty Vs My Melody House Design 🍭💕 | Toca Life World | Toca Tanya'


def parce_args():
    parce_arg = argparse.ArgumentParser(description='function')
    parce_arg.add_argument('-f', dest='functions', required=True)
    parce_arg.add_argument('-arg', dest='arguments', default='')
    return parce_arg.parse_args()


def browser(target_url, proxy, name_video, time_low, time_max):
    pr = prototipe.prototipe(target_url=target_url, proxy=proxy, name_video=name_video)
    pr.go(time_low=time_low, time_max=time_max)


def start_view_video(args):
    command, thread_count = args.split(':')
    if command == 'Play':
        for _ in range(int(thread_count+1)):
            ThreadingVideo = threading.Thread(
                target=browser, 
                args=(target_url, '154.16.243.167:6311:ctimpebr:anssq5y9ocac', name_video, 16, 25)
                )
            ThreadingVideo.start()
            time.sleep(random.randint(8, 15))

def add_proxy(args):
    path_proxy_list, path_db = args.split(':')
    db = database.sql(path=path_db)
    with open(path_proxy_list, 'r', newline='\r\n') as file:
        for id, line in enumerate(file.readlines()):
            proxy = line[:-2]
            if db.check_proxy(proxy=proxy)[0]==0:
                db.add_proxy(proxy=proxy)



def main():
    FUNCTIONS_LIST = {
    'View_videos': start_view_video,
    'Add_proxy': add_proxy,
    }   
    args = parce_args()
    if str(args.functions) in FUNCTIONS_LIST:
        FUNCTIONS_LIST[args.functions](args.arguments)


if __name__ == '__main__':
    main()