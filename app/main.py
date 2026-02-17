from script import run
from config import DEVICE_ID, DEVICE_TOKEN, API_URL, PUSH_INTERVAL, DECIBEL_OFFSET

if __name__ == "__main__":
    run(device_id=DEVICE_ID,
        device_token=DEVICE_TOKEN,
        api_url=API_URL,
        push_interval=PUSH_INTERVAL,
        decibel_offset=DECIBEL_OFFSET)
