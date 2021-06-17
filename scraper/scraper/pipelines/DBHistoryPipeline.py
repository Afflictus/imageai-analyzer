import sqlite3
from config import DATABASE_PATH


class DBHistoryPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE if not exists history
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            analyzed BOOL,
            banned BOOL,
            UNIQUE (url) ON CONFLICT IGNORE);
        """)
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO history (url, analyzed, banned) VALUES(?, ?, ?)
        """, (item['url'], False, False))
        self.connection.commit()
        self.cursor.execute("""
            SELECT id FROM history
            where url=?
        """, (item['url'],))
        item['history_id'] = (self.cursor.fetchone())[0]
        return item
