import isodate
import datetime
import os
from googleapiclient.discovery import build


class PlayList:
    """Создаем класс 'PlayList'"""
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        """
        Реализуем инициализацияю_id_ плейлиста, которая имеет следующие публичные атрибуты:
        - название плейлиста
        - ссылку на плейлист
        """
        self.playlist_id = playlist_id
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.playlists = self.youtube.playlists().list(id=playlist_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.title = self.playlists["items"][0]["snippet"]["title"]
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)
                                                         ).execute()

    @property
    def total_duration(self):
        """
        Возвращает объект класса `datetime.timedelta` с суммарной длительностью плейлиста
        """
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        max_like = 0
        max_video = ""
        for video in self.video_response['items']:
            count_like = video['statistics']['likeCount']
            count_video = video['id']
            if int(count_like) > int(max_like):
                max_video = count_video
        return f"https://youtu.be/{max_video}"
