import requests
import time
from config import Config

class ThreadsPoster:
    def __init__(self):
        self.access_token = Config.THREADS_ACCESS_TOKEN
        self.user_id = Config.THREADS_USER_ID
        self.base_url = "https://graph.threads.net/v1.0"

    def create_post(self, text):
        """Create a Threads post"""

        # Step 1: Create media container
        container_url = f"{self.base_url}/{self.user_id}/threads"

        params = {
            'media_type': 'TEXT',
            'text': text,
            'access_token': self.access_token
        }

        try:
            response = requests.post(container_url, params=params)
            response.raise_for_status()
            container_id = response.json()['id']

            # Step 2: Publish the container
            publish_url = f"{self.base_url}/{self.user_id}/threads_publish"
            publish_params = {
                'creation_id': container_id,
                'access_token': self.access_token
            }

            # Wait a moment before publishing
            time.sleep(1)

            publish_response = requests.post(publish_url, params=publish_params)
            publish_response.raise_for_status()

            return {
                'success': True,
                'thread_id': publish_response.json()['id']
            }

        except requests.exceptions.RequestException as e:
            # Try to get more details from the response
            error_detail = str(e)
            try:
                if hasattr(e, 'response') and e.response is not None:
                    error_json = e.response.json()
                    error_detail = f"{e} - API Response: {error_json}"
            except:
                pass
            return {
                'success': False,
                'error': error_detail
            }
