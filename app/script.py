import pyaudio
import time
import numpy as np
from math import log10
import requests

# audio settings - mic is in Card2
p = pyaudio.PyAudio()
FORMAT = pyaudio.paInt32  # 32bit
RATE = 48000
CHANNELS = 2
CHUNK = 4096
DEVICE = 1
rms = 1e-10


def callback(in_data):
    global rms
    # bytes to numpy array
    audio_data = np.frombuffer(in_data, dtype=np.int32)
    rms = np.sqrt(np.mean(audio_data ** 2)) / (2 ** 31)
    return in_data, pyaudio.paContinue


def run(device_id: int, device_token: str, api_url: str, push_interval: float, decibel_offset: float) -> None:
    stream = p.open(format=FORMAT,
                    input_device_index=DEVICE,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=False,
                    stream_callback=callback)

    stream.start_stream()
    print("ctr+c to stop")
    try:
        while stream.is_active():
            if rms > 0:
                db: float = 20 * log10(rms)
                try:
                    headers = {
                        "XDevice-ID": device_id,
                        "XDevice-Token": device_token
                    }
                    payload = {
                        "decibel_val": db + float(decibel_offset)
                    }
                    requests.post(api_url, headers=headers, json=payload)
                    time.sleep(push_interval)
                except Exception as e:
                    raise Exception("Failed to push reading", e)
                print(f"RMS: {rms:.6f} | dB: {db:.2f} dB")
    except KeyboardInterrupt:
        print("\nending...")

    stream.stop_stream()
    stream.close()
    p.terminate()
