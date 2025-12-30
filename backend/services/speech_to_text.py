import assemblyai as aai
from config import ASSEMBLYAI_API_KEY

aai.settings.api_key = ASSEMBLYAI_API_KEY

def transcribe_audio(file_path):
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)
        return transcript.text if transcript.text else None
    except:
        return None
