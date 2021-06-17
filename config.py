import os

# root path
ROOT = os.path.dirname(os.path.abspath(__file__))
# path to hosts file filder
HOSTS_FOLDER = os.path.join(ROOT, "app")
# path to hosts file
HOSTS_PATH = os.path.join(ROOT, HOSTS_FOLDER, "hosts")
# path to main backup file
BACKUP_HOSTS_FILE = os.path.join(ROOT, HOSTS_FOLDER, "blocker_hosts")
# allowed sites
ALLOWED = [
    'ya.ru',
    'yandex.',
    'google.',
    'youtube.',
    'vk.com'
]
# path to working database
DATABASE_PATH = os.path.join(ROOT, "app", "data.db")
# model for object detection
DETECTION_MODEL = os.path.join(ROOT, "analyzer", "model.h5")
# path to save downloaded images for analyze
DOWNLOADER_IMAGES = os.path.join(ROOT, "analyzer", "images")
