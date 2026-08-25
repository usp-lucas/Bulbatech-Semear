"""
Propósito único de obter os frames e melhorar o framerate
Extremamente útil em hardware limitado
"""
import threading
from threading import Thread
import cv2 as cv
import time
import logging

class VideoStream:
    """Objeto de video"""
    def __init__(self, resolucao=(1280,720), taxaquadros=30, NoteOuWebcam=1, src=0, API=200):
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

        
        self.stream = cv.VideoCapture(src, apiPreference=200)
        
        if isinstance(resolucao, (tuple, list)) and len(resolucao) >= 2:
            
            self.stream.set(cv.CAP_PROP_FRAME_WIDTH, resolucao[0])
            self.stream.set(cv.CAP_PROP_FRAME_HEIGHT, resolucao[1])
        else:
            self.logger.warning("Formato de resolução inválido. Usando padrão de hardware.")
            
        self.stream.set(cv.CAP_PROP_FPS, taxaquadros)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        """bool: Variavel para controlar se a câmera parou"""
        self.lock = threading.Lock()
        self.logger.info("Módulo VideoStream inicializado")
    def comeca(self):
        """
        Inicia as thread para a leitura de frames
        """
        t = Thread(target=self.atualizacao,name="VideoStreamThread",daemon=True) 
        t.start()
        self.logger.info("Thread de aquisição de vídeo iniciada com sucesso.")
        return self
    def atualizacao(self):
        while not self.stopped:
            (grabbed, frame) = self.stream.read()
            if not grabbed:
                self.logger.error("Falha física de comunicação com o sensor da câmera. Interrompendo captura.")
                self.pare()
                break
                
            # Escrita segura protegida por Mutex Lock
            with self.lock:
                self.frame = frame
    def leia(self):
        # Leitura segura protegida por Mutex Lock
        with self.lock:
            # Evita sobrescrever os pixels
            return self.frame.copy() if self.frame is not None else None

    def pare(self):
        self.stopped = True
        self.stream.release()
        self.logger.info("Recursos de captura de vídeo liberados de forma segura.")