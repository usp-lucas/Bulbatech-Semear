from typing import Final

### Caminhos
#Originamento te um 'r' antes do caminho
RECOGNIZER_MODEL_PATH : Final = "/home/yobenjas/Semear/Bulbatech-Semear/vosk-model-small-pt-0.3/"
VOICE_MODEL_PATH : Final = "/home/yobenjas/Semear/Bulbatech-Semear/voiceModel/pt_BR-jeff-medium.onnx"
VOICE_CONFIG_PATH : Final = "/home/yobenjas/Semear/Bulbatech-Semear/voiceModel/pt_BR-jeff-medium.onnx.json"
BULBASAUR_VIT_AUDIO_PATH: Final = "/home/yobenjas/Semear/Bulbatech-Semear/voiceFiles/"

### Configurações de escuta
DEVICE_INDEX : Final = 4
AUDIO_FREQUENCY = 48000
BUFFER_SIZE = 4096 #Originalmente 8192
AUDIO_VOCABULARY: Final = ["clima", "horas", "bom dia", "desligar", "sabedoria", "[unk]"]

