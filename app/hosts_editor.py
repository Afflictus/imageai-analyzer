from config import HOSTS_PATH, BACKUP_HOSTS_FILE, HOSTS_FOLDER
from shutil import copy2
from config import *
import os.path
import sqlite3
import os


class HostsEditor:
    def __init__(self):
        self.__PATH = HOSTS_PATH
        self.__BACKUP_FILE = BACKUP_HOSTS_FILE

    def check_backup(self):
        if not os.path.isfile(self.__BACKUP_FILE):
            copy2(self.__PATH, self.__BACKUP_FILE)

    def check_blocked(self):
        start_end_indexes = []
        with open(self.__PATH, 'r') as f:
            contents = f.readlines()

        for index, line in enumerate(contents):
            if "###### BLOCKER_START ######\n" == line:
                start_end_indexes.append(index + 1)
            if "###### BLOCKER_END ######\n" == line:
                start_end_indexes.append(index)

        return tuple(start_end_indexes)

    def show_blocked(self):
        indexes = self.check_blocked()
        with open(self.__PATH, 'r') as f:
            contents = f.readlines()
        print(contents[indexes[0]:indexes[1]])

    @staticmethod
    def __rename_sites(sites, string):
        return [string + i for i in sites]

    def __bd_get_sites(self):
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT DISTINCT(h.url) FROM history h
                WHERE h.banned = true
            """)
            sites = [i[0] for i in cursor.fetchall()]
            sites = self.__rename_sites(sites, "0.0.0.0 ")
            return sites
        except Exception as e:
            return []

    def bd_write_sites(self):
        self.check_backup()
        indexes = self.check_blocked()
        sites = self.__bd_get_sites()

        if not indexes:
            with open(self.__PATH, "a") as f:
                f.write("\n###### BLOCKER_START ######\n")
                f.write('\n'.join(sites) + '\n')
                f.write("###### BLOCKER_END ######\n\n")
        else:
            with open(self.__PATH, 'r') as f:
                contents = f.readlines()
            sites = [i for i in sites if i + "\n" not in contents]
            if sites:
                contents.insert(indexes[0], '\n'.join(sites) + '\n')

                with open(self.__PATH, 'w') as f:
                    contents = ''.join(contents)
                    f.write(contents)

    def restore_hosts(self):
        with open(self.__BACKUP_FILE, 'r') as f:
            contents = f.readlines()

        with open(self.__PATH, 'w')as f:
            contents = ''.join(contents)
            f.write(contents)

    def make_backup(self):
        from datetime import datetime
        now = datetime.now().strftime(" %d_%m_%Y_%H_%M_%S")

        try:
            copy2(self.__PATH, self.__BACKUP_FILE + now)
            return True, "--> Файл бекапа успшно создан\n"
        except Exception as e:
            print(e)
            return False, "--. Ошибка при создании файла бекапа\n" \
                          "Подробности: " + str(e) + "\n"


edit = HostsEditor()
print(edit.show_blocked())
