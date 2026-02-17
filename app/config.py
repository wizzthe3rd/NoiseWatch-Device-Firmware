from dotenv import load_dotenv
import os

load_dotenv()

DEVICE_ID = os.getenv("DEVICE_ID")
DEVICE_TOKEN = os.getenv("DEVICE_TOKEN")
API_URL = os.getenv("API_URL")
PUSH_INTERVAL = os.getenv("PUSH_INTERVAL")  # interval between noise requests sent to api in seconds
DECIBEL_OFFSET = os.getenv("DECIBEL_OFFSET")  # added to readings to make decibel vals more readable


