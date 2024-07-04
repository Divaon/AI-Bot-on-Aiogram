from check_file import check_and_generate_file_name
from settings import client

# return audio with our text
async def text_to_audio(text):
    responces = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    file_name = await check_and_generate_file_name("output")
    responces.stream_to_file(file_name)
    return file_name