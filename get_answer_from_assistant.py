import time

from settings import client, config

# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run



# send question to assistant
async def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )




# return response from assistant
async def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

# make tread of assistant
async def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run =  await submit_message(config.ASSISTANT_ID, thread, user_input)
    return thread, run

# return answer of assistant
async def get_answer(question):
    thread, run = await create_thread_and_run(question)
    run = wait_on_run(run, thread)
    response = await get_response(thread)
    for answer in response:
        if answer.role == "assistant":
            return answer.content[0].text.value
    return "Извините. Я не смог обдумать ответ"

