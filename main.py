from distutils import command
import prototipe
import threading
import time
import random
import argparse
from termcolor import colored
import database
import re


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


def add_video(args):
    https, target_url, name_video, time_min, time_max, thread, count, path_db =  args.split(":")
    target_url = https + target_url
    print(f'{target_url=} {name_video=} {time_min=} {time_max=}')
    db = database.sql(path=path_db)
    db.add_video(target_url, name_video, time_min, time_max, thread, count)


def start_view_video(args):
    command, path_db = args.split(':')
    db = database.sql(path=path_db)
    PROXY_LIST = db.get_proxy_avalible()
    
    VIDEO_LIST = db.get_videos()

    for VIDEO in VIDEO_LIST:
        if command == 'Play':
            for _ in range(int(VIDEO[5])):
                ThreadingVideo = threading.Thread(
                    target=browser, 
                    args=(VIDEO[1], random.choices(PROXY_LIST)[0][1], VIDEO[2], int(VIDEO[3]), int(VIDEO[4]))
                    )
                ThreadingVideo.start()
                time.sleep(random.randint(33, 56))


def add_proxy(args):
    path_proxy_list, path_db = args.split(':')
    db = database.sql(path=path_db)
    with open(path_proxy_list, 'r', newline='\r\n') as file:
        for line in file.readlines():
            proxy = line[:-2]
            if db.check_proxy(proxy=proxy)[0]==0:
                db.add_proxy(proxy=proxy)


def main():
    FUNCTIONS_LIST = {
    'View_videos': start_view_video,
    'Add_proxy': add_proxy,
    'Add_video': add_video,
    }   
    args = parce_args()
    if str(args.functions) in FUNCTIONS_LIST:
        FUNCTIONS_LIST[args.functions](args.arguments)


if __name__ == '__main__':
    main()