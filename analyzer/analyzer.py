from config import DETECTION_MODEL, DOWNLOADER_IMAGES, DATABASE_PATH
from imageai.Detection import ObjectDetection
import requests
import sqlite3
import os
import pathlib


class Analyzer:
    def __init__(self):
        self.init = False
        self.model_path = None
        self.detector = None
        self.urls = []

    def initialize(self, model_path=DETECTION_MODEL):
        self.model_path = model_path
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath(self.model_path)
        self.detector.loadModel()
        self.init = True
        return True, "--> Модуль Analyzer инициализирован и готов к работе\n"

    def set_default(self):
        self.initialize()
        return True, "--> Установлены настройки анализатора по умолчанию\n"

    def set_model_path(self, model_path):
        path = pathlib.Path(str(model_path))
        if path.exists() and path.is_dir():
            self.model_path = model_path
            self.detector.setModelPath(self.model_path)
            return True, "--> Путь к модели установлен\n"
        else:
            return False, f"--> Путь к модели не был установлен. " \
                          f"Проверьте правильность пути {str(model_path)}\n"

    def initialize_custom(self):
        self.detector.loadModel()
        self.init = True
        return True, "--> Модель инициализирована"

    def set_model_type(self):
        print("1. RetinaNet\n2. YOLOv3\n3. TinyYOLOv3\n")
        model_type = input("Введите номер модели\n>>> ")
        if model_type == "1":
            self.detector.setModelTypeAsRetinaNet()
        elif model_type == "2":
            self.detector.setModelTypeAsYOLOv3()
        elif model_type == "3":
            self.detector.setModelTypeAsTinyYOLOv3()
        else:
            return False, "--> Тип модели не изменен\n"
        return True, "--> Тип модели изменен\n"

    def get_preferences(self):
        preferences = f"--> Путь до модели: {str(self.detector.modelPath)}\n" \
                      f"--> Тип модели: {str(self.detector._ObjectDetection__modelType)}"
        print(preferences)

    def __db_write_image(self, url):
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        try:
            cursor.execute("""
                UPDATE images
                SET analyzed = 1
                WHERE image_url=?
            """, (url,))
            connection.commit()
            return True, "--> Запись в таблицу images: успешно\n"
        except Exception as e:
            return False, "--> Запись в таблицу images: провалено\nПодробности: " + str(e) + "\n"

    def __db_write_history(self, url):
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        try:
            cursor.execute("""
                update history
                set banned = 1,
                    analyzed = 1
                where id in (SELECT
                   url from images where analyzed = 1 and image_url = ?)
            """, (url,))
            connection.commit()
            return True, "--> Запись в таблицу history: успешно\n"
        except Exception as e:
            return False, "--> Запись в таблицу history: провалено\nПодробности: " + str(e) + "\n"

    def __db_write_ban_images(self):
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        print(
            "--> Запись в таблицу images: обновление метки analyzed всех изображений, расположенных на странице с "
            "запрещенным контентом")
        try:
            cursor.execute("""
                update images
                set analyzed = 1
                where url in (SELECT id from history
                where banned = 1)
            """)
            connection.commit()
            return True, "--> Запись в таблицу images: успешно\n"
        except Exception as e:
            return False, "--> Запись в таблицу images: провалено\nПодробности: " + str(e) + "\n"

    def download(self, url):
        try:
            response = requests.get(url)
        except Exception as e:
            return False, "--> Не удалось загрузить изображение\nПодробности: " + str(e) + "\n"

        image_path = os.path.join(DOWNLOADER_IMAGES, "1.jpg")
        with open(image_path, "wb") as f:
            f.write(response.content)
        return True, image_path

    def __db_read_images(self):
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT image_url from images
                where analyzed = false
            """)
            urls = [i[0] for i in cursor.fetchall()]
            return True, urls
        except Exception as e:
            return False, "--> Чтение из таблицы images: ошибка\nПодробности: " + str(e) + "\n"

    def analyze_all(self):
        urls = self.__db_read_images()[1]
        if len(urls) == 0:
            print("--> Отсутствуют изображения для анализа")
            return
        for index, url in enumerate(urls):
            print(f"--> Анализ изобаржения {index + 1} из {len(urls)}")
            self.analyze(url)
        return self.urls

    def analyze(self, url):
        if not self.init:
            print("--> Анализатор не инициализирован.")
            print("--> Инициализация...")
            self.initialize()
        try:
            image_path = self.download(url)
            if not image_path[0]:
                raise Exception(image_path[1])

            image_path = image_path[1]
            save_path = os.path.join(DOWNLOADER_IMAGES, '1_detected.jpg')
            custom_objects = self.detector.CustomObjects(bottle=True)
            detections = self.detector.detectObjectsFromImage(custom_objects=custom_objects,
                                                              input_image=image_path,
                                                              minimum_percentage_probability=50,
                                                              output_image_path=save_path)
            self.__db_write_image(url)
            for eachObject in detections:
                if eachObject['name'] == 'bottle':
                    self.__db_write_history(url)
                    self.__db_write_ban_images()
                    self.urls.append(url)
                    print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ",
                          eachObject["box_points"])
                    print("--------------------------------")
        except Exception as e:
            self.__db_write_image(url)
            print("--> Во время анализа изображений произошла ошибка\nПодробности: " + str(e))

