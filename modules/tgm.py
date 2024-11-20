import requests
import os
import re
import json
import modules.handle_json as handle_json


class Bot:
    """A class to interact with Telegram Bot API."""
    
    def __init__(self, auth_token, chat_id):
        """Initialize bot with authentication token and chat ID."""
        self.auth_token = auth_token
        self.chat_id = chat_id
        self.base_url = f'https://api.telegram.org/bot{self.auth_token}'
        handle_json.create_config()

    def get_update(self, param='all'):
        """Get updates from Telegram API."""

        offset = handle_json.single_element('offset')
        url_params = {"offset" : offset}
        response = requests.get(f'{self.base_url}/getUpdates',url_params)
        result = response.json()
        if result['result']:
            offset = result['result'][-1]['update_id']
            print('offset :',offset)
            handle_json.single_element('offset',offset+1)
        else:
            pass

        if param == 'chat_id':
            return result["result"][0]["message"]["chat"]["id"]
        elif param == 'all':
            return result
        else:
            print('Options:\n  all : entire JSON\n  chat_id : group chat ID')
        
        self.send_msg('bot restarted')

    def recive_msg(self):
        """Fetch the last messages sent to the bot, limited to the specified number."""

        offset = handle_json.single_element('offset')
        url_params = {"offset": offset}

        response = requests.get(f'{self.base_url}/getUpdates', url_params)
        result = response.json()

        if result['result']:  # Check if there are any messages
            handle_json.update_offset()
            messages = result.get("result", [])
            recent_messages = messages
            
            # Extract text messages only, skipping messages without text
            return [
                (msg["message"]["chat"]["id"], msg["message"].get("text"))
                for msg in recent_messages
                if "message" in msg and "text" in msg["message"]
            ]
        else:
            pass


    def send_msg(self, msg):
        """Send a text message to the chat."""
        params = {"chat_id": self.chat_id, "text": msg}
        requests.get(f'{self.base_url}/sendMessage', params=params)

    def send_photo(self, file_path):
        """Send a photo file to the chat."""
        if self._validate_file(file_path, r'.jpg|.png|.jpeg|.gif|.webp'):
            with open(file_path, 'rb') as file:
                files = {"photo": file}
                params = {"chat_id": self.chat_id}
                response = requests.post(
                    f'{self.base_url}/sendPhoto',
                    params=params,
                    files=files
                )
                print(f'Sent: {os.path.basename(file_path)}')
                return response.status_code == 200
        return False

    def send_vid(self, file_path):
        """Send a video file to the chat."""
        if self._validate_file(file_path, r'.mp4|.mov|.avi|.mkv|.wmv') and \
           os.path.getsize(file_path) < 50 * 1024 * 1024:
            with open(file_path, 'rb') as file:
                files = {"video": file}
                params = {"chat_id": self.chat_id}
                response = requests.post(
                    f'{self.base_url}/sendVideo',
                    params=params,
                    files=files
                )
                print(f'Sent: {os.path.basename(file_path)}')
                return response.status_code == 200
        print('File too large or invalid format.')
        return False

    def send_media_group(self, media_files):
        """Send multiple media files as a group."""
        media = []
        files = {}

        for file_path in media_files:
            if os.path.exists(file_path) and \
               os.path.getsize(file_path) < 50 * 1024 * 1024:
                media_type = "photo" if re.search(r'.jpg|.png|.jpeg|.gif', file_path) \
                           else "video"
                media.append({
                    "type": media_type,
                    "media": f"attach://{os.path.basename(file_path)}"
                })
                files[os.path.basename(file_path)] = open(file_path, 'rb')
            else:
                print(f'Skipping {file_path} (invalid format or too large)')

        if media:
            data = {
                "chat_id": self.chat_id,
                "media": json.dumps(media)
            }
            response = requests.post(
                f'{self.base_url}/sendMediaGroup',
                data=data,
                files=files
            )
            for f in files.values():
                f.close()
            return response.json()
        print('No valid media to send.')
        return None

    def _validate_file(self, file_path, pattern):
        """Validate if file exists and matches the given pattern."""
        if not os.path.exists(file_path):
            print(f'File does not exist: {file_path}')
            return False
        if not re.search(pattern, file_path):
            print(f'Invalid file type for {file_path}')
            return False
        return True