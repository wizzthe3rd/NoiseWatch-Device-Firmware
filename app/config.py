from dotenv import load_dotenv
import os

load_dotenv()

DEVICE_ID = os.get_env("DEVICE_ID")
DEVICE_SECRET = os.get_env("DEVICE_SECRET")
API_URL = os.get_env("API_URL")


