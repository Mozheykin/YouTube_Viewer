import threading
import multiprocessing
import time
import random
import argparse
# from app import database, prototipe
import database
import prototipe
from loguru import logger


logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', 
            rotation='10 MB', compression='zip')

locker = threading.Lock()
THREAD_COUNT = 5
NAME_DB = 'sqlite.db'


def parce_args():
    parce_arg = argparse.ArgumentParser(description='function')
    parce_arg.add_argument('-f', dest='functions', required=True)
    parce_arg.add_argument('-arg', dest='arguments', default='')
    return parce_arg.parse_args()


def browser(target_url, proxy, name_video, time_low, time_max, id, path_db, pool):
    with pool:
        pr = prototipe.prototipe(target_url=target_url, proxy=proxy, name_video=name_video)
        db = database.sql(path=path_db)
        name_thr = threading.current_thread().name
        name_process = multiprocessing.current_process().name
        logger.info(f'{name_thr=}, {name_process=}')
        if pr.go(time_low=time_low, time_max=time_max):
            with locker:
                db.update_count(db.video(id)[6] + 1, id)
        db.close()


def video_procces(VIDEO: list, path_db: str):
    pool = threading.BoundedSemaphore(value=THREAD_COUNT)
    db = database.sql(path=path_db)
    PROXY_LIST = db.get_proxy_avalible()
    while  db.video(VIDEO[0])[6] < int(VIDEO[8]):
        proxy_choice = random.choices(PROXY_LIST)[0][1]
        ThreadingVideo = threading.Thread(
            target=browser, 
            args=(VIDEO[2], proxy_choice, VIDEO[3], int(VIDEO[4]), int(VIDEO[5]), int(VIDEO[0]), path_db, pool),
            name=f'thread {VIDEO[3]}',
            )
        ThreadingVideo.start()
        time.sleep(5)


def add_video(args):
    https, target_url, name_video, time_min, time_max, thread, count, path_db =  args.split(":")
    target_url = https + target_url
    print(f'{target_url=} {name_video=} {time_min=} {time_max=}')
    db = database.sql(path=path_db)
    db.add_video(target_url, name_video, time_min, time_max, thread, count)


def start_view_video(args):
    try:
        path_db = args
        db = database.sql(path=path_db)
        VIDEO_LIST = db.get_videos()
        with multiprocessing.Pool(multiprocessing.cpu_count() * 2) as p:
            p.map(lambda VIDEO: video_procces(VIDEO, path_db), VIDEO_LIST)
    except Exception as ex:
        print(ex)


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
