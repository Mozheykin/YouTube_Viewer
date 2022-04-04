import sqlite3


class sql:
    def __init__(self, path='sqlite.db', view_table='statistic_video', proxy_table='proxy_table') -> None:
        self.view_table = view_table
        self.proxy_table = proxy_table
        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()
        try:
            with self.db:
                self.db.execute(f'''CREATE TABLE IF NOT EXISTS {self.view_table}(
                    video_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
                    created DATETIME NOT NULL,
                    url VARCHAR(255),
                    name VARCHAR(255),
                    min_view INTEGER NOT NULL,
                    max_view INTEGER NOT NULL,
                    count_view INTEGER NOT NULL,
                    avalible BOOL NOT NULL,
                    thread INTEGER NOT NULL)
                    ''')
                self.db.execute(f'''CREATE TABLE IF NOT EXISTS {self.proxy_table}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    proxy TEXT,
                    avalible BOOL)
                    ''')
                
        except self.db.Error as ex:
            print(ex)
        self.db.commit()
    
    def __enter__(self):
        return self

    def add_proxy(self, proxy:str):
        with self.db:
            return self.cursor.execute(f'INSERT INTO {self.proxy_table}(proxy, avalible) VALUES(?,?)', (proxy, True))
    
    def check_proxy(self, proxy:str):
        with self.db:
            return self.cursor.execute(f'SELECT COUNT(id) as count FROM {self.proxy_table} WHERE proxy=?', (proxy,)).fetchone()
    
    def update_avalible_proxy(self, avalible:bool, id:int):
        with self.db:
            return self.cursor.execute(f'UPDATE {self.proxy_table} SET avalible=? WHERE id=?', (avalible, id))
    
    def get_proxy_avalible(self):
        with self.db:
            return self.cursor.execute(f'SELECT *  FROM {self.proxy_table} WHERE avalible=?', (True,)).fetchall()
    
    def add_video(self, target_url, name, min, max, thread, count):
        with self.db:
            return self.cursor.execute(
                f'INSERT INTO {self.view_table}(url, name, min_view, max_view, thread, count_view, avalible) VALUES(?,?,?,?,?,?,?)',
                (target_url, name, min, max, thread, count, True)
                )
    
    def get_videos(self):
        with self.db:
            return self.cursor.execute(f'SELECT * FROM {self.view_table} WHERE avalible=?', (True,)).fetchall()
    
    def video(self, video_id):
        with self.db:
            return self.cursor.execute(f'SELECT * FROM {self.view_table} WHERE video_id=?', (video_id,)).fetchone()
    
    def update_count(self, count, id):
        with self.db:
            return self.cursor.execute(f'UPDATE {self.view_table} SET count_view=? WHERE video_id=?', (count, id))
    
    def __exit__(self, *args, **kwargs):
        self.db.commit()
        self.db.close()
