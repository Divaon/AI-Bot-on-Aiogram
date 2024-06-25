from settings import client


# return text from audio file
async def audio_to_text(audio_file_name):
    audio_file = open(audio_file_name, "rb")
    transcription = await client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcription.text
