##-------------Código Principal---------

##Bibliotecas necessárias
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import constantes


##Configurando modelo
model = Model(constantes.MODEL_PATH)
recognizer = KaldiRecognizer(model, constantes.AUDIO_FREQUENCY)
##Configurando o microfone
microphone = pyaudio.PyAudio()
stream = microphone.open(
    format=pyaudio.paInt16,
    channels=1,
    rate = constantes.AUDIO_FREQUENCY,
    input=True,
    input_device_index=constantes.DEVICE_INDEX,
    frames_per_buffer=constantes.BUFFER_SIZE
    )
##Inicia a escuta
stream.start_stream()
print("Ouvindo...")
##Interpreta o áudio
while True:
    data = stream.read(constantes.BUFFER_SIZE, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        resultado = json.loads(recognizer.Result())
        print("Você disse:", resultado["text"])

##Teste de palavras reconhecidas
# while True:
#     data = stream.read(constantes.BUFFER_SIZE, exception_on_overflow=False)

#     if recognizer.AcceptWaveform(data):
#         resultado = json.loads(recognizer.Result())
#         print("FRASE FINAL:", resultado["text"])

#     else:
#         parcial = json.loads(recognizer.PartialResult())
#         print("PARCIAL:", parcial["partial"])