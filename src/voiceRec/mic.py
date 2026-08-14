import pyaudio

audio = pyaudio.PyAudio()

print("DISPOSITIVOS DE ENTRADA:\n")

for i in range(audio.get_device_count()):
    info = audio.get_device_info_by_index(i)

    if info["maxInputChannels"] > 0:
        print(f"ID: {i}")
        print(f"Nome: {info['name']}")
        print(f"Canais: {info['maxInputChannels']}")
        print(f"Sample Rate: {info['defaultSampleRate']}")
        print()

audio.terminate()