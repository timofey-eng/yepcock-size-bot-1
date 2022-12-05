import json
import os
import subprocess
from datetime import datetime

from vosk import KaldiRecognizer, Model


class STT:
    default_init = {
        "model_path": "models/vosk",
        "sample_rate": 16000,
    }

    def __init__(self,
                 model_path=None,
                 sample_rate=None,
                 ffmpeg_path=None
                 ) -> None:
        self.model_path = model_path if model_path else STT.default_init["model_path"]
        self.sample_rate = sample_rate if sample_rate else STT.default_init["sample_rate"]

        model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(model, self.sample_rate)
        self.recognizer.SetWords(True)


    def audio_to_text(self, audio_file_name=None) -> str:
        process = subprocess.Popen(
            ["ffmpeg",
             "-loglevel", "quiet",
             "-i", audio_file_name,
             "-ar", str(self.sample_rate),
             "-ac", "1",
             "-f", "s16le",
             "-"
             ],
            stdout=subprocess.PIPE
                                   )

        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                pass

        result_json = self.recognizer.FinalResult()
        result_dict = json.loads(result_json)
        return result_dict["text"]
