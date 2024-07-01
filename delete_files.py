import asyncio
import os

# delete mp3 file from root
async def delete_mp3_file_from_root(file_name):
    if file_name.endswith(".mp3"):
        await asyncio.to_thread(os.remove, file_name)
    else:
        for files in os.walk("."):
            for file in files[2]:
                if file.endswith(".mp3") and file.startswith(file_name):
                    await asyncio.to_thread(os.remove, file)
            return
    return

# delete all mp3 files from project root
async def delete_all_mp3_files_from_root():
    for files in os.walk("."):
        for file in files[2]:
            if file.endswith(".mp3"):
                await asyncio.to_thread(os.remove, file)
        return