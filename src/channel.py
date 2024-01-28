import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    API_KEY:str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.channel)