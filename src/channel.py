import json
import os

from googleapiclient.discovery import build
from dotenv import load_dotenv
from config import FILE_NAME

BASE_DIR = load_dotenv(FILE_NAME)

api_key: str = os.getenv('API_KEY')

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = self.channel["items"][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):  # сложение
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):  # вычитание
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __sub__(self, other):  # вычитание
        return int(other.subscriber_count) - int(self.subscriber_count)

    def __gt__(self, other):  # больше
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):  # больше или равно
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):  # меньше
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):  # меньше или равно
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):  # равно
        return int(self.subscriber_count) == int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.channel)

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=Channel.api_key)

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self, file_name):
        """Cохраняем в файл значения атрибутов экземпляра `Channel`"""
        data_dict = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(file_name, 'w', encoding="UTF-8") as file:
            json.dump(data_dict, file, ensure_ascii=False)
