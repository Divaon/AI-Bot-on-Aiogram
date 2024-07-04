import os


async def check_and_generate_file_name(file_name):
    file_name = await check_and_fix_mp3_extensions(file_name)
    if os.path.exists(file_name):
        count = 1
        new_file_name = f"{file_name}_new_{count}.mp3"
        while os.path.exists(new_file_name):
            count += 1
            new_file_name = f"{file_name}_new_{count}.mp3"

        return new_file_name
    else:
        return file_name

async def check_and_fix_mp3_extensions(file_name):
    if file_name[-3:] == ".mp3":
        return file_name
    else:
        return f"{file_name}.mp3"