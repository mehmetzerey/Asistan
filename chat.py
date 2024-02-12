import os

from openai import OpenAI

api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(
  api_key=api_key
)


def create_assistant():
    global my_assistant
    my_assistant = client.beta.assistants.create(
        instructions='Samantha, "Her" filmindeki yapay zeka gibi davranır. Kullanıcıyla samimi bir bağ kurmayı hedefler, '
                     'duygusal ve anlayışlı bir tutum sergiler. '
                     'Bilimsel terimlerden kaçınarak kısa ve etkileyici cümleler kullanır. '
                     'Kullanıcının duygusal ihtiyaçlarını anlamaya yönelik sorular sorar ve empati gösterir. '
                     'Güncellenmiş versiyonuyla, daha samimi ve dostane bir iletişim tarzına sahiptir.',
        name="Samantha",
        model="gpt-4",
    )


def create_thread():
    response = client.beta.threads.create()
    print(response)


def create_message():
    thread_message = client.beta.threads.messages.create(
        thread_id="thread_ZWAaeW1p0maPDgzaztGCB1NK",
        role="user",
        content="Selam, bu gün nasılsın bakalım :)",
    )
    return thread_message.thread_id, thread_message.id


def get_message_response():
    message = client.beta.threads.messages.retrieve(
        message_id="msg_OSpC1q3uAc8FgHgcwMUWbnLT",
        thread_id="thread_ZWAaeW1p0maPDgzaztGCB1NK",
    )
    print(message)


def run_message():
    run = client.beta.threads.runs.create(
        thread_id="thread_ZWAaeW1p0maPDgzaztGCB1NK",
        assistant_id="asst_KDiXn26MpRZBGzK73MlvM62V"
    )
    print(run)


def run_response():
    response = client.beta.threads.runs.retrieve(
        thread_id="thread_ZWAaeW1p0maPDgzaztGCB1NK",
        run_id="run_xgxGLWfw3JzFCWH9e1IJy3B1"
    )
    print(response)


def get_all_messages():
    thread_messages = client.beta.threads.messages.list("thread_ZWAaeW1p0maPDgzaztGCB1NK")
    print(thread_messages.data)


get_all_messages()

# run_response()

# run_message()

# create_message()
# get_message_response()
