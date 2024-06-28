from settings import client

# return audio with our text
async def text_to_audio(text):
    responces = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    responces.stream_to_file("output.mp3")
    return "output.mp3"