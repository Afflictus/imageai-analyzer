import sqlite3
from config import DATABASE_PATH


class DBImagePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE if not exists images
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_url TEXT,
            analyzed BOOL,
            url INTEGER,
            FOREIGN KEY(url) REFERENCES history(id));
        """)
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        for image in item['images']:
            self.cursor.execute("""
                INSERT INTO images (image_url, analyzed, url) VALUES(?, ?, ?)
            """, (image, False, item['history_id']))
            self.connection.commit()
        return item
