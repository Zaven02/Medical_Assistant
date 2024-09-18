import os
import requests
from flask import Flask, request
from models.text_extraction import extract_text
from models.llm import get_gpt4_response
from database.db_setup import engine, get_db_session
from database.models import User, FileRecord
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TOKEN = os.getenv('TOKEN')
LOCAL_URL = "https://d69a-78-109-73-33.ngrok-free.app/webhook"  # can be ngrok URL
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"


@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    print(update)

    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']

        # Extract nickname and name
        from_user = message.get('from', {})
        username = from_user.get('username') or None
        first_name = from_user.get('first_name', '') or None
        last_name = from_user.get('last_name', '') or None
        userData = {
            'id': chat_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name
        }

        name = first_name

        if 'text' in message:
            message_text = message['text']
            contents = get_file_contents_by_chat_id(chat_id)
            print({'contents': contents})
            response_text = get_gpt4_response(message_text, contents)
            send_message(chat_id, response_text)

        elif 'document' in message:
            file_id = message['document']['file_id']
            mime_type = message['document']['mime_type']
            file_name = message['document']['file_name']

            # Only accept PDFs
            if mime_type == 'application/pdf':
                file_path = get_file_path(file_id)
                if file_path:
                    file_full_path = download_file(file_path, file_name)
                    content = extract_text(file_full_path)
                    file_data = {
                        'id': file_id,
                        'file_type': mime_type,
                        'file_name': file_name,
                        'content': content
                    }
                    save_file_to_db(userData, file_data)
                    send_message('Saved Successfully')
            else:
                send_message(chat_id, "Unsupported message type. Please send text, PDF, PNG, or JPEG.")

        # Check if it's a photo (PNG, JPEG)
        elif 'photo' in message:
            file_id = message['photo'][-1]['file_id']  # Highest resolution
            file_path = get_file_path(file_id)
            if file_path:
                file_name = f"{file_id}.jpg"
                file_full_path = download_file(file_path, file_name)
                content = extract_text(file_full_path)
                file_data = {
                    'id': file_id,
                    'file_type': 'image',
                    'file_name': file_name,
                    'content': content
                }
                save_file_to_db(userData, file_data)
                send_message(chat_id, "Image saved successfully.")

        # Unsupported message type
        else:
            send_message(chat_id, "Unsupported message type. Please send text, PDF, PNG, or JPEG.")

    return '', 200


@app.route('/set-webhook', methods=['POST'])
def setwebhook():
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook"

    # Make the request to set the webhook
    response = requests.post(TELEGRAM_API_URL, data={'url': LOCAL_URL})

    # Print the response
    print(response.json())

    return '', 200


def get_file_path(file_id):
    url = f"{TELEGRAM_API_URL}/getFile?file_id={file_id}"
    response = requests.get(url)
    if response.status_code == 200:
        file_info = response.json()
        return file_info['result']['file_path']
    return None


def download_file(file_path, file_name):
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    response = requests.get(file_url, stream=True)

    data_folder = os.path.join(os.path.dirname(__file__), 'storage')

    if response.status_code == 200:
        file_full_path = os.path.join(data_folder, file_name)
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        with open(file_full_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return file_full_path
    return None


def save_file_to_db(user_data, file_data):
    # Get a database session
    session = get_db_session()

    chat_id = user_data.get('id')
    username = user_data.get('username')
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')

    file_id = file_data.get('id')
    file_name = file_data.get('file_name')
    file_type = file_data.get('file_type')
    content = file_data.get('content')

    try:
        user = session.query(User).filter_by(id=chat_id).first()
        if not user:
            user = User(
                id=chat_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            session.add(user)
            session.commit()

        file_record = FileRecord(id=file_id, user_id=chat_id, file_name=file_name, file_type=file_type, content=content)

        session.add(file_record)

        session.commit()

        print(f"File '{file_name}' saved successfully for user with chat_id '{chat_id}'.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


def get_file_contents_by_chat_id(chat_id):
    session = get_db_session()
    try:
        file_records = session.query(FileRecord).filter_by(user_id=chat_id).all()
        contents = [file_record.content for file_record in file_records if file_record.content]
        return contents
    except Exception as e:
        print(f"An error occurred while fetching file records for chat_id {chat_id}: {e}")
        return []
    finally:
        session.close()


def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(TELEGRAM_API_URL + "/sendMessage", json=payload)
    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(f"Response: {response.text}")


if __name__ == '__main__':
    app.run(port=5000)
