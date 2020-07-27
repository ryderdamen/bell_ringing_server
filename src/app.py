import os
from urllib.parse import urlencode
from flask import Flask
import requests
from dotenv import load_dotenv
from datetime import datetime
from bs4 import BeautifulSoup


load_dotenv()
app = Flask(__name__)


@app.route('/bell')
def bell():
    if should_bell_ring():
        return "ring"
    return ""


@app.route('/')
def index():
    return ""


def get_sub_count_from_youtube():
    """Returns the subscriber count"""
    base = 'https://www.googleapis.com'
    endpoint = '/youtube/v3/channels'
    params = {
        'part': 'statistics',
        'id': os.environ.get('YOUTUBE_CHANNEL_ID'),
        'key': os.environ.get('YOUTUBE_API_KEY')
    }
    url = base + endpoint + '?' + urlencode(params)
    response = requests.get(url)
    if not response.status_code == 200:
        raise Exception('Status code not 200')
    return int(response.json()['items'][0]['statistics']['subscriberCount'])


def get_sub_count():
    """Returns a cached subscriber count every 30 minutes"""
    global last_fetched_from_youtube
    global cached_youtube_subscriber_count
    delta = datetime.now() - last_fetched_from_youtube
    if int(delta.seconds) > 1800:
        live_sub_count = get_sub_count_from_youtube()
        cached_youtube_subscriber_count = live_sub_count
        last_fetched_from_youtube = datetime.now()
    return cached_youtube_subscriber_count


def should_bell_ring():
    """Determines if the bell should ring or not this request"""
    global displayed_subscriber_count
    actual_sub_count = get_sub_count()
    if actual_sub_count > displayed_subscriber_count:
        displayed_subscriber_count += 1
        return True
    return False


last_fetched_from_youtube = datetime.now()
last_fetched_from_tiktok = datetime.now()
cached_youtube_subscriber_count = get_sub_count_from_youtube()
total_cached_subscriber_count = cached_youtube_subscriber_count
displayed_subscriber_count = total_cached_subscriber_count


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
