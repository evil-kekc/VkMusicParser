import logging
import os
import shutil

import vk_api
from dotenv import load_dotenv
from vk_api.audio import VkAudio


class VkMusicParser:
    def __init__(self, login: str, password: str):
        """Gets all audio recordings from all playlists on the page in VK and writes audio recordings to text files

        :param login: login from VK
        :param password: password from VK
        """
        self.vk_audio = None
        self.login = login
        self.password = password
        self.vk_session = vk_api.VkApi(self.login, self.password)
        self.playlists = list()
        self.logger = self._setup_logger()

        if os.path.exists('data'):
            shutil.rmtree('data')

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger('parser')
        logger.setLevel(logging.INFO)

        if not os.path.exists('logs'):
            os.makedirs('logs')

        log_file = os.path.join(os.path.abspath(os.curdir), 'logs/parser.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    def _write_results_to_file(self, filename: str, artist: str, title: str) -> None:
        """Writes audio recordings from playlists to a file with the name of the playlist

        :param filename: file name (playlist name)
        :param artist: artist name
        :param title: song name
        :return: None
        """
        if not os.path.exists('data'):
            os.makedirs('data')
            self.logger.info('Create directory [data]')

        with open(fr'data/{filename}.txt', 'a', encoding='utf-8') as file:
            file.write(f'{artist} - {title}\n')

    def _get_playlists(self) -> list[dict]:
        """Getting a list of playlist names and their id

        :return: playlist list
        """
        for index, album in enumerate(self.vk_audio.get_albums_iter()):
            self.playlists.append({
                'id': album.get('id'),
                'title': album.get('title')
            })
        return self.playlists

    def _get_music_from_playlist(self, album_id: int, title: str) -> None:
        """Getting music from a playlist and transferring song titles for recording

        :param album_id: album id with music
        :param title: album title
        :return:
        """
        music = self.vk_audio.get(album_id=album_id)
        for audio in music:
            self._write_results_to_file(filename=title, artist=audio.get('artist'), title=audio.get('title'))

    def get_vk_audio_from_playlists(self) -> None:
        """Getting music from playlists

        :return: None
        """
        try:
            self.vk_session.auth()
        except vk_api.AuthError as error_msg:
            self.logger.error(error_msg)
            return

        self.vk_audio = VkAudio(self.vk_session)
        playlists = self._get_playlists()

        for playlist in playlists:
            self._get_music_from_playlist(album_id=playlist['id'], title=playlist['title'])


if __name__ == '__main__':
    load_dotenv()
    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    app = VkMusicParser(login=login, password=password)
    app.get_vk_audio_from_playlists()
