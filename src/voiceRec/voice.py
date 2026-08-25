##-------------Código Principal---------
##Bibliotecas gerais
from datetime import datetime
import constantes
import random

##Bibliotecas STT
from vosk import Model, KaldiRecognizer
import pyaudio
import json

##Bibliotecas TTS
from piper import PiperVoice
import sounddevice as sd
import numpy as np
import wave

##Bibliotecas de vitalidade
from pydub import AudioSegment

#Toca um arquivo wav (duh)
def tocar_wav(caminho):
    with wave.open(caminho, "rb") as wf:
        sample_rate = wf.getframerate()
        n_channels = wf.getnchannels()
        audio = wf.readframes(wf.getnframes())
        audio_np = np.frombuffer(audio, dtype=np.int16)
        if n_channels == 2:
            audio_np = audio_np.reshape(-1, 2)
        audio_np = audio_np.astype(np.float32) / 32768.0
        sd.play(audio_np, sample_rate)
        sd.wait()

#Função auxiliar para resposta dos comandos
def falar(texto, arquivo="resposta.wav", printTXT=True):
    if(printTXT):
        print(f"Bulbatech do Mal: {texto}")
    with wave.open(arquivo, "wb") as wav_file:
        jeff_voice.synthesize_wav(texto, wav_file)
    tocar_wav(arquivo)

def gritinho():
    try:
        ##Inicialização
        num = random.randint(0,4)#Gera um número aleatório para escolher o audio
        arquivo_aleatorio = f"{constantes.BULBASAUR_VIT_AUDIO_PATH}{num}.mp3"
        audio = AudioSegment.from_mp3(arquivo_aleatorio)
        data_audio = np.array(audio.get_array_of_samples(), dtype=np.float32)
        #Normalização de audio
        if audio.sample_width == 2:
            data_audio /= 32768.0
        elif audio.sample_width == 1:
            data_audio = (data_audio - 128.0) / 128.0
        if audio.channels == 2:
            data_audio = data_audio.reshape((-1,2))

        #Toca o áudio
        sd.play(data_audio, audio.frame_rate)
    except Exception as e:
        print(f"Erro ao dar gritinho: {e}")

#=====Configuração de Voz e Vitalidade=======
#Configurando modelo de reconhecimento
model = Model(constantes.RECOGNIZER_MODEL_PATH)
vocabulary = json.dumps(constantes.AUDIO_VOCABULARY)
recognizer = KaldiRecognizer(model, constantes.AUDIO_FREQUENCY, vocabulary)
gritinho()

#Configurando o microfone
microphone = pyaudio.PyAudio()
stream = microphone.open(
    format=pyaudio.paInt16,
    channels=1,
    rate = constantes.AUDIO_FREQUENCY,
    input=True,
    input_device_index=constantes.DEVICE_INDEX,
    frames_per_buffer=constantes.BUFFER_SIZE
    )

#=====Configuração de Fala=======
jeff_voice = PiperVoice.load(constantes.VOICE_MODEL_PATH, config_path=constantes.VOICE_CONFIG_PATH)
print("Bulbatech do Mal: Olá, eu sou o Bulbatech! Como vão as coisas?")
falar("Olá, eu sou o Bulbatek! Como vão as coisas?", printTXT=False)

#=====Código Principal===========
##Inicia a escuta
stream.start_stream()
print("Estou te ouvindo...")

##Interpreta o áudio
timer = 0
while True:
    if timer >200:
        gritinho()
        timer = 0

    timer+=1
    data = stream.read(constantes.BUFFER_SIZE, exception_on_overflow=False)
    
    if recognizer.AcceptWaveform(data):
        resultado = json.loads(recognizer.Result())
        comando = resultado.get("text", "").strip().lower()
        
        print("Você disse:", comando)
        ##if not comando:
        ##    continue  #tratamento de silêncio/ruído

        if "clima" in comando:
            falar("Hoje tá muito, muito quente!")
        if "bom dia" in comando:
            falar("Bom dia! O Tibas tá por aí?")
        elif "sabedoria" in comando:
            falar("Nunca deixe de ser mau por causa das pessoas boas")
        elif "horas" in comando:
            agora = datetime.now()
            texto_hora = agora.strftime("Agora são %H horas e %M minutos.")
            falar(texto_hora)
        elif "desligar" in comando:
            falar("Até mais, amigo")
            break

#Fecha tudo :P
stream.stop_stream()
stream.close()
microphone.terminate()