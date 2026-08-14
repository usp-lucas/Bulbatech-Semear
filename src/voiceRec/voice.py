##-------------Código Principal---------

##Bibliotecas necessárias
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import constantes


##Configurando modelo
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, AUDIO_FREQUENCY)
##Configurando o microfone
microphone = pyaudio.PyAudio()
stream = microphone.open(
    format=pyaudio.paInt16,
    channels=1,
    rate = AUDIO_FREQUENCY,
    input=True,
    input_device_index=DEVICE_INDEX,
    frames_per_buffer=8192
    )
##Inicia a escuta
stream.start_stream()
print("Ouvindo...")
##Interpreta o áudio
while True:
    data = stream.read(4396, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        resultado = json.loads(recognizer.Result())
        print("Você disse:", resultado["text"])