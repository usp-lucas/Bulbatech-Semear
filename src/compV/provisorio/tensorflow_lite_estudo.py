import numpy as np
import cv2 as cv
from ai_edge_litert.interpreter import Interpreter

class PercepcaoVisual:
    def __init__(self, modelo, debug=True):
        self.interpretador = Interpreter(model_path=modelo)
        self.interpretador.allocate_tensors

        self.detalhes_entrada = self.interpretador.get_input_details()
        self.detalhes_saida = self.interpretador.get_output_details()

        self.indice_entrada = self.detalhes_entrada[0].get("index")
        self.largura_entrada = self.detalhes_entrada[0].get("shape")[2]
        self.altura_entrada = self.detalhes_entrada[0].get("shape")[1]

    def inferir(self, quadro):
        TAMANHO_QUADRO = (self.largura_entrada,self.altura_entrada)
        quadro_redimensionado = cv.resize(quadro,TAMANHO_QUADRO,interpolation=cv.INTER_LINEAR)
        quadro_rgb = cv.cvtColor(quadro_redimensionado,cv.COLOR_BGR2RGB)
        quadro_rgb.insert(0,1)
