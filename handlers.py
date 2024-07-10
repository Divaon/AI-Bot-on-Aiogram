import asyncio

from aiogram import Router
from aiogram.types import ContentType, FSInputFile
from aiogram.filters import Command
from aiogram.types import Message
import delete_files
from audio_to_text import audio_to_text
from check_file import check_and_generate_file_name
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
    file_name = await check_and_generate_file_name("voice_message")
    file = await bot.download_file(file_path, file_name)
    return file_name

async def processing_voice_message(message: Message):
    voice_file_id = message.voice.file_id
    try:
        mp3_file = await convert_voice_to_mp3(voice_file_id)
        answer = await get_answer_on_voice_message(mp3_file)
        answer_file = FSInputFile(answer)
        await message.answer_audio(audio=answer_file)
        await delete_files.delete_mp3_file_from_root(mp3_file)
        await delete_files.delete_mp3_file_from_root(answer)
    except Exception as e:
        await message.answer(f"При обработке голосового сообщения возникли проблемы.")

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Отправь мне голосовое сообщение, и я постараюсь его обработать.")

@router.message()
async def voice_message_handler(message: Message):
    if message.content_type == ContentType.VOICE:
        asyncio.create_task(processing_voice_message(message))
    else:
        await message.answer(f"Твой ID: {message.from_user.id}. Я работаю с голосовыми, а не с текстовыми сообщениями.")
