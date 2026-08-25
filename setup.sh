#Instala dependência de áudio
sudo apt update
sudo apt install portaudio19-dev python3-dev gcc
#Definindo Ambiente Virtual ------->(Só rode na pasta certa, colega)<------
sudo apt install python3-venv python3-full -y
python3 -m venv env
source env/bin/activate
###instala biblioteca
pip install pyaudio
pip install vosk
pip install sounddevice numpy
pip install piper-tts
pip install miniaudio
pip install just-playback
pip install pydub
#pip install pyaudio vosk
#pip install sounddevice numpy piper-tts
