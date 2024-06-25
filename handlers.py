import os
from aiogram import Router, Bot
from aiogram.types import ContentType, FSInputFile
from aiogram.filters import Command
from aiogram.types import Message
from settings import config

router = Router()


bot = Bot(token=config.TOKEN_API)

async def convert_voice_to_mp3(voice_file_id):
    file = await bot.get_file(voice_file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "voice_message.mp3")
    return 'voice_message.mp3'

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Отправь мне голосовое сообщение, и я постараюсь его обработать.")

@router.message()
async def voice_message_handler(message: Message):
    if message.content_type == ContentType.VOICE:
        voice_file_id = message.voice.file_id
        mp3_file = await convert_voice_to_mp3(voice_file_id)
        audio_file = FSInputFile(mp3_file)
        await message.answer_audio(audio=audio_file)
        os.remove(mp3_file)
        await message.answer(f"Я получил голосовое сообщение от вас.")
    else:
        await message.answer(f"Твой ID: {message.from_user.id}. Я работаю с голосовыми, а не с текстовыми сообщениями.")


