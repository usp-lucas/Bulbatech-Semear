#Instala dependência de áudio e vídeo
sudo apt update && sudo apt install python3-venv python3-full libopencv-dev python3-opencv -y
sudo apt install portaudio19-dev python3-dev gcc
#Definindo Ambiente Virtual (Só rode na pasta certa, colega)
python3 -m venv env
source env/bin/activate
###instala biblioteca
pip install pyaudio
pip install vosk
pip install opencv-python
