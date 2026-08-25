"""
Propósito único de obter os frames e melhorar o framerate
Extremamente útil em hardware limitado
"""
from threading import Thread, Lock
import cv2 as cv
import time
import logging

class FluxoVideo:
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
        self.logger = logging.getLogger(self.__class__.__name__)
        self.NoteOuWebcam = NoteOuWebcam 
        self.taxaquadros = taxaquadros
        self.resolucao = resolucao

        
        self.fluxo = cv.VideoCapture(src, cv.CAP_V4L2)
        
        if isinstance(resolucao, (tuple, list)) and len(resolucao) >= 2:
            self.fluxo.set(cv.CAP_PROP_FRAME_WIDTH, resolucao[0])
            self.fluxo.set(cv.CAP_PROP_FRAME_HEIGHT, resolucao[1])
        else:
            self.logger.warning("Formato de resolução inválido. Usando padrão de hardware.")
        # Pendente: tratamento de erros
        self.fluxo.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
        self.fluxo.set(cv.CAP_PROP_FPS, taxaquadros)
        self.fluxo.set(cv.CAP_PROP_AUTO_EXPOSURE, 0.25)
        self.fluxo.set(cv.CAP_PROP_AUTO_WB, 0)

        (self.grabbed, self.frame) = self.fluxo.read()
        self.stopped = False
        """bool: Variavel para controlar se a câmera parou"""
        self.lock = Lock()
        """locktype: """
        self.logger.info("Módulo FluxoVideo inicializado")
    def comeca(self):
        """
        Inicia as thread para a leitura de frames
        """
        thread = Thread(target=self.atualizacao,name="FluxoVideoThread",daemon=True) 
        thread.start()
        self.logger.info("Thread de aquisição de vídeo iniciada com sucesso.")
        return self
    def atualizacao(self):
        while not self.stopped:
            (capturado, frame) = self.fluxo.read()
            if not capturado:
                self.logger.error("Falha física de comunicação com o sensor da câmera. Interrompendo captura.")
                self.pare()
                break

            with self.lock:
                self.frame = frame
    def leia(self):
        with self.lock:
            # Evita sobrescrever os pixels
            return self.frame.copy() if self.frame is not None else None

    def pare(self):
        self.stopped = True
        self.fluxo.release()
        self.logger.info("Recursos de captura de vídeo liberados de forma segura.")