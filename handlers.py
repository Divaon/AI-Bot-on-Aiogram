import os


from aiogram import Router
from aiogram.types import ContentType, FSInputFile
from aiogram.filters import Command
from aiogram.types import Message
from audio_to_text import audio_to_text
from get_answer_from_assistant import get_answer
from settings import bot
from text_to_audio import text_to_audio

router = Router()


async def get_answer_on_voice_message(audio_file):
    text_audio = await audio_to_text(audio_file)
    answer = await get_answer(text_audio)
    answer_file = await text_to_audio(answer)
    return answer_file

async def convert_voice_to_mp3(voice_file_id):
    file = await bot.get_file(voice_file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "voice_message.mp3")
    return "voice_message.mp3"

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Отправь мне голосовое сообщение, и я постараюсь его обработать.")

@router.message()
async def voice_message_handler(message: Message):
    if message.content_type == ContentType.VOICE:
        voice_file_id = message.voice.file_id
        try:
            mp3_file = await convert_voice_to_mp3(voice_file_id)
            answer = await get_answer_on_voice_message(mp3_file)
            answer_file = FSInputFile(answer)
            await message.answer_audio(audio=answer_file)
            os.remove(mp3_file)
            os.remove(answer)
            await message.answer(f"Я получил голосовое сообщение от вас.")
        except Exception as e:
            await message.answer(f"При обработке голосового сообщения возникли проблемы.")
    else:
        await message.answer(f"Твой ID: {message.from_user.id}. Я работаю с голосовыми, а не с текстовыми сообщениями.")
