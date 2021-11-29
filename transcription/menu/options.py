from typing import Iterable
from pytube import YouTube
from pytube.query import StreamQuery, Stream
from transcription.menu.imenu import MenuOption
from PyInquirer import prompt

from transcription.menu.questions.audio_questions import QUESTION_TAG, QUESTION_URL


class DownloadAudioOption(MenuOption):
    """
    Esta opción permite descargar audio desde un video de youtube.
    """

    def __init__(self, next_option: MenuOption):
        super().__init__(next_option)

    def execute(self, option: str):
        if option == "download_yt_audio":
            yt: YouTube = self._select_video()

            stream_list: Iterable[Stream] = yt.streams.filter(only_audio=True)
            
            stream: Stream = self._select_stream(yt, stream_list)
            stream.download()
            print("¡Su audio ha sido descargado de forma exitosa!")
        else:
            self.next_option.execute(option)

    def _select_video(self):
        url = prompt(QUESTION_URL)["url"]
        yt = YouTube(url)
        print("El video que usted eligió es: " + yt.title)
        return yt

    def _select_stream(self, yt: YouTube, stream_list: Iterable[Stream]):
        stream_question = self.generate_stream_choices(stream_list)    
        tag = int(prompt(stream_question)['tag_option'])
        stream = yt.streams.get_by_itag(tag)
        return stream

    def generate_stream_choices(self, stream_list: Iterable[Stream]):
        stream_choices = [
                {
                    "name": f"abr: {stream.abr} | codec: {stream.audio_codec} | extension: {stream.mime_type}",
                    "value": stream.itag,
                }
                for stream in stream_list
            ]
        QUESTION_TAG[0]["choices"] = stream_choices
        return QUESTION_TAG


class DownloadAudioAndVideoOption(DownloadAudioOption):
    """
    Esta opción permite descargar audio y video desde un video de youtube.
    """

    def __init__(self, next_option: MenuOption):
        super().__init__(next_option)
    
    def execute(self, option: str):
        if option == "download_yt_audio_and_video":
            yt: YouTube = self._select_video()

            stream_list: Iterable[Stream] = yt.streams.filter(progressive=True)
            
            stream: Stream = self._select_stream(yt, stream_list)
            stream.download()
            print("¡Su audio ha sido descargado de forma exitosa!")
        else:
            self.next_option.execute(option)