from browser_history import get_history as gt
from config import ALLOWED


class History:
    def __init__(self, allowed=ALLOWED):
        self.history = []
        self.allowed = allowed

    def clear_history(self):
        try:
            self.history = []
            return True, "История очищена\n"
        except Exception as e:
            return False, "Во время очистки истории произошла ошибка\nПодробности" + str(e) + "\n"

    @staticmethod
    def __adding(outputs: list, allowed):
        """ Make list without duplicates
        and allowed sites"""
        res = []
        for index, value in enumerate(outputs):
            if value not in res:
                if not any(i in value for i in allowed):
                    res.append(value)
        return res

    def get_history(self):
        """ Return browser history list of urls"""
        try:
            outputs = [i[1] for i in gt().histories]
            res = self.__adding(outputs, self.allowed)
            self.history = res
            return True, "История браузеров загружена"
        except Exception as e:
            return False, "Во время загрузки истории браузеров " \
                          "произошла ошибка\nПодробности" + str(e) + "\n"



