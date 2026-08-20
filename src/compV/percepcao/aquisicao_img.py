"""
Propósito único de obter os frames e melhorar o framerate
Extremamente útil em hardware limitado
"""
from threading import Thread
import cv2 as cv
import time

class VideoStream:
    """Objeto de video"""
    def __init__(self, resolucao=(1280,720), taxaquadros=30, NoteOuWebcam=1, src=0):
        """
        Args:
            resolucao (tuple): Define a tupla(W,H) da resolução da câmera,
            Default=(1280,720)
            framerate (int): Define o framerate da câmera, Default=30
            NoteOrWebcam (int): Entre 1 ou 2 para qual câmera está sendo cap-
            turada, Default = 1
            src (int): Indice do componente físico de captura,
            Default=0 
        """
        self.NoteOuWebcam = NoteOuWebcam #Define a variável para o NoteOrWebcam

        if self.NoteOuWebcam in (1,2):
            self.stream = cv.VideoCapture(src)
            # parâmetros físicos da câmera, width(largura) e height(altura) ambos int.
            self.stream.set(cv.CAP_PROP_FRAME_WIDTH, resolucao[0])
            self.stream.set(cv.CAP_PROP_FRAME_HEIGHT, resolucao[1])
            self.stream.set(cv.CAP_PROP_FPS, taxaquadros)
            # Tenta desativar autoexposição e correção de branco (da câmera)
            self.stream.set(cv.CAP_PROP_AUTO_EXPOSURE, 0.25) 
            self.stream.set(cv.CAP_PROP_AUTO_WB, 0)
            # lê o primeiro frame
            (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        """bool: Variable to control when camera is stopped"""
    def comeca(self):
        """
        Inicia as thread para a leitura de frames
        """
        Thread(target=self.atualizacao,args=(),daemon=True).start()
        return self
    def atualizacao(self):
        if self.NoteOuWebcam in (1,2):
            # loop indefinitivo até a thread parar
            while True:
                #Mutuamente para a thread, se a camera tambem parar
                if self.stopped:
                    self.stream.release()
                    return
                # Caso contrário, adquiri o próximo frame
                (self.grabbed, self.frame)=self.stream.read()
                # importante dar um tempinho pro processamento hehe
                time.sleep(0.001)
    def leia(self):
        # Retorna o frame mais atualizado
        return self.frame
    def pare(self):
        # Indica que a camera e o thread pararam
        self.stopped = True