<<<<<<< HEAD
#Instala dependência de áudio
sudo apt update
sudo apt install portaudio19-dev python3-dev gcc
#Definindo Ambiente Virtual ------->(Só rode na pasta certa, colega)<------
sudo apt install python3-venv python3-full -y
=======
#Instala dependência de áudio e vídeo
sudo apt update && sudo apt install python3-venv python3-full libopencv-dev python3-opencv -y
sudo apt install portaudio19-dev python3-dev gcc
#Definindo Ambiente Virtual (Só rode na pasta certa, colega)
>>>>>>> b80fb31 (Cria módulos iniciais de Visão Computacional.)
python3 -m venv env
source env/bin/activate
###instala biblioteca
pip install pyaudio
pip install vosk
<<<<<<< HEAD
pip install sounddevice numpy
pip install piper-tts
pip install pydub
#pip install pyaudio vosk
#pip install sounddevice numpy piper-tts
=======
pip install opencv-python
>>>>>>> b80fb31 (Cria módulos iniciais de Visão Computacional.)
