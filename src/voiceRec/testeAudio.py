import pyaudio
import wave

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=48000,
                     input=True, input_device_index=4, frames_per_buffer=4096)

frames = []
print("Gravando 10s...")
for _ in range(0, int(48000 / 4096 * 10)):
    frames.append(stream.read(4096, exception_on_overflow=False))

stream.stop_stream()
stream.close()
audio.terminate()

wf = wave.open("teste.wav", "wb")
wf.setnchannels(1)
wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
wf.setframerate(48000)
wf.writeframes(b"".join(frames))
wf.close()
print("Salvo teste.wav")