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
DEVICE = 2
rms = 1e-10


def callback(in_data, frame_count, time_info, status):
    global rms
    audio_data = np.frombuffer(in_data, dtype=np.int32).astype(np.float64)
    audio_data /= np.iinfo(np.int32).max
    rms = np.sqrt(np.mean(audio_data ** 2))
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
            time.sleep(push_interval)

            print(f"[DEBUG] raw rms={rms:.8f}")

            if rms <= 1e-6:
                continue

            db_raw: float = 20 * log10(rms)
            if db_raw <= -100:
                continue

            db: float = db_raw + decibel_offset
            print(f"RMS: {rms:.6f} | dB: {db:.2f} dB")

            try:
                headers = {
                    "XDevice-ID": device_id,
                    "XDevice-Token": device_token
                }
                payload = {
                    "decibel_val": db
                }
                requests.post(api_url, headers=headers, json=payload, timeout=2)
            except Exception as e:
                print(f"Push failed: {e}")

    except KeyboardInterrupt:
        print("\nending...")

    stream.stop_stream()
    stream.close()
    p.terminate()
