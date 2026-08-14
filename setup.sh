#Instala dependência de áudio
sudo apt install portaudio19-dev python3-dev gcc
#Definindo Ambiente Virtual (Só rode na pasta certa, colega)
sudo apt update && sudo apt install python3-venv python3-full -y
python3 -m venv env
source env/bin/activate
###instala biblioteca
pip install pyaudio
pip install vosk
