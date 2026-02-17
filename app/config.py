from dotenv import load_dotenv
import os

load_dotenv()

DEVICE_ID = os.get_env("DEVICE_ID")
DEVICE_TOKEN = os.get_env("DEVICE_TOKEN")
API_URL = os.get_env("API_URL")
PUSH_INTERVAL = os.getenv("PUSH_INTERVAL")  # interval between noise requests sent to api
DECIBEL_OFFSET = os.getenv("DECIBEL_OFFSET")  # added to readings to make decibel vals more readable


