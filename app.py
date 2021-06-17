from app.history import History
from app.hosts_editor import HostsEditor
from analyzer.analyzer import Analyzer
from scraper.scraper_app import scrap
from config import DATABASE_PATH
import sqlite3


class UI:
    def __init__(self):
        self.analyzer = Analyzer()
        self.history = History()
        self.hosts_editor = HostsEditor()

    def __print_menu(self):
        print("\n1. Настройка анализатора")
        print("2. Настройка списка скрапинга")
        print("3. Запустить скрапинг сайтов")
        print("4. Запустить анализ сайтов")
        print("5. Блокировка сайтов")
        print("0. Закрыть программу")

    def __menu_history(self):
        loop = True
        menu = "--- Настройка списка сайтов для скрапинга\n" \
               "1. Загрузить историю браузеров\n" \
               "2. Добавить сайт для скрапинга\n" \
               "3. Вывести список сайтов для скрапинга\n" \
               "4. Очистить список\n" \
               "0. Вернуться\n"

        while loop:
            print(menu)
            choose = input("Введите номер операции\n>>> ")

            if choose == "1":
                print(self.history.get_history()[1])
            elif choose == "2":
                self.history.history.append(input("Введите адрес сайта\n>>> "))
            elif choose == "3":
                print(self.history.history)
            elif choose == "4":
                print(self.history.clear_history()[1])
            elif choose == "0":
                loop = False

    def __menu_analyzer(self):
        loop = True
        menu = "--- Настройка анализатора\n" \
               "--- Перед изменением настроек необходимо инициализировать модель\n" \
               "1. Установить путь до модели\n" \
               "2. Установить тип модели\n" \
               "3. Вывести информацию о настройках анализатора\n" \
               "4. Установить настройки по умолчанию\n" \
               "5. Инициализировать модель\n" \
               "0. Вернуться\n"

        while loop:
            print(menu)
            choose = input("Введите номер операции\n>>> ")
            try:
                if choose == "1":
                    path = input("Введите путь до модели\n>>> ")
                    print(self.analyzer.set_model_path(path)[1])
                elif choose == "2":
                    print(self.analyzer.set_model_type()[1])
                elif choose == "3":
                    self.analyzer.get_preferences()
                elif choose == "4":
                    print(self.analyzer.set_default()[1])
                elif choose == "5":
                    self.analyzer.initialize()
                elif choose == "0":
                    loop = False
            except Exception as e:
                print(e)

    def start(self):
        loop = True
        while loop:
            self.__print_menu()
            choose = input(">>> ")

            if choose == '1':
                self.__menu_analyzer()
            elif choose == '2':
                self.__menu_history()
            elif choose == '3':
                if self.history.history:
                    scrap(self.history.history)
                    print("Скрапинг завершен.")
                else:
                    print("--> Список для сканирования пуст.")
            elif choose == '4':
                self.analyzer.analyze_all()
            elif choose == '5':
                print("Блокировка сайтов")
            elif choose == '0':
                loop = False


if __name__ == "__main__":
    app = UI()
    app.start()
