from settings import client


async def audio_to_text(audio_file_name):
     with open(audio_file_name, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file)
        return transcription.text

