import cv2 as cv
import numpy as np
from threading import Thread, Lock

class AquisicaoCamera:
    def __init__(self, resolucao=(1280,720), taxa_quadros=30, endereco_camera=0):
            self.resolucao = resolucao
            self.taxa_quadros = taxa_quadros
            self.endereco_camera = endereco_camera
            self.lock = Lock()

            self.fluxo_video = cv.VideoCapture(endereco_camera)
            (self.obtido, self.quadro) = self.fluxo_video.read()
            self.parado = False
    def atualizar(self):
          while not self.parado:
            obtido, quadro = self.fluxo_video.read()
            with self.lock:
                self.obtido, self.quadro = obtido, quadro
    def iniciar(self):
         encadeamento_execucao = Thread(target=self.atualizar,args=(),daemon=True)
         encadeamento_execucao.start()
    def parar(self):
         self.parado = True
         self.fluxo_video.release()
    def ler(self):
         with self.lock:
              return self.quadro