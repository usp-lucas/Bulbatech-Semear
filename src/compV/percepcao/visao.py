"""
Trata matrizes e quadros
"""
import cv2 as cv
import numpy as np
import logging
class PercepcaoVisual:
    def __init__(self, debug=False):
        self.debug = debug
        self.logger = logging.getLogger(self.__class__.__name__)
        self.colors_hsv =  {
            "SOL": {
                "lower": np.array([153, 141, 2], dtype=np.uint8),
                "upper": np.array([224, 169, 60], dtype=np.uint8)
            },
            "NUVEM": {
                "lower": np.array([17, 71, 136], dtype=np.uint8),
                "upper": np.array([122, 143, 181], dtype=np.uint8)
            }
        }
        # Kernel para as operações morfológicas (formato elíptico é melhor para formas orgânicas)
        # cv.MORPH_RECT, para retângulos
        self.kernel_morfologia = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
        self.logger.info('[SUCCESS] Instanciamento de PercepcaoVisual')
    def pre_process(self, quadro, largura=320, altura=240):
        """
        Método que aplica processamento ao quadro bruto, retorna o novo quadro
        melhor otimizado.
        """
        if quadro is None or quadro.size == 0:
            self.logger.warning("Quadro invalido recebido do Pré-processamento. Retornando None.")
            return None
        try:
            return cv.resize(quadro, (largura,altura),interpolation=cv.INTER_LINEAR)
        except Exception as e:
            self.logger.error(f"Falha ao redimensionar quadro: {e}", exc_info=True)
            return None
    def cria_masc_cor(self, quadro_hsv, nome_alvo):
        """
        Método que consome um quadro em HSV e retorna uma máscara binária,
        conforme o nome alvo.
        """
        if quadro_hsv is None:
            return
        if nome_alvo not in self.colors_hsv:
            raise KeyError(f"Alvo '{nome_alvo}' não configurado no dicionário de cores.")
        try:    
            target_upper = self.colors_hsv[nome_alvo].get("upper")
            target_lower = self.colors_hsv[nome_alvo].get("lower")
            masc = cv.inRange(quadro_hsv,target_lower,target_upper)
            # Opening (remove ruído de fundo) e Closing (preenche buracos no alvo)
            masc = cv.morphologyEx(masc, cv.MORPH_OPEN, self.kernel_morfologia)
            masc = cv.morphologyEx(masc, cv.MORPH_CLOSE, self.kernel_morfologia)
            return masc
        except Exception as e:
            self.logger.error(f"Erro ao processar máscara de cor para {nome_alvo}: {e}")
            return None
    def extrai_valores_geometricos(self, masc, alvo_cubico=True):
        """
        Método que calcula contornos, o centroide do contorno de maior area
        e retorna os valores do ponto, area e se é maior que um limitrófe
        """
        contornos,_ = cv.findContours(masc,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if contornos:
            cnt = max(contornos,key=cv.contourArea)
            contornos_area = cv.contourArea(cnt)

            M = cv.moments(cnt)
            cx,cy = 0,0
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"]) 

            emaior = contornos_area > 100.0
            forma_valida = True

            if alvo_cubico and emaior:
                envoltoria = cv.convexHull(cnt)
                area_envol = cv.contourArea(envoltoria)

                if area_envol > 0:

                    indice_solidez = contornos_area / float(area_envol)

                    forma_valida = indice_solidez > 0.85

                else:
                    forma_valida = False
            alvo_confirmado = emaior and forma_valida
            return {"centroide": (cx,cy), "area_cnt": contornos_area, "alvo_confirmado": alvo_confirmado}
        return {"centroide": (0,0), "area_cnt": 0.0, "alvo_confirmado": False}
    def canaliza_process(self, quadro, nome_alvo):
        """
        Método unificado que consome um quadro bruto, executa todas as etapas
        e retorna as coordenadas puras para a tomada de decisão do robô.
        """

        quadro_pre_proces = self.pre_process(quadro)
        if quadro_pre_proces is None:
            return {"alvo_encontrado": False, "erro_pre_proces": True}
        quadro_hsv = cv.cvtColor(quadro_pre_proces, cv.COLOR_BGR2HSV)
        masc = self.cria_masc_cor(quadro_hsv, nome_alvo)
        geom_info = self.extrai_valores_geometricos(masc, alvo_cubico=True)

        if self.debug:
            foiconfirmado = geom_info.get("alvo_confirmado")
            coords_cen = geom_info.get("centroide")
            if foiconfirmado:
                red = (0,0,255)
                cv.circle(quadro_pre_proces, coords_cen,5,red,-1)

                # Desenha-se o contorno retangular envolvente ao alvo
                contornos, _ = cv.findContours(masc, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                if contornos:
                    cnt = max(contornos, key=cv.contourArea)
                    x, y, w, h = cv.boundingRect(cnt)
                    cv.rectangle(quadro_pre_proces, (x, y), (x+w, y+h), (0, 255, 0), 2)

            quadro_mascarado = cv.bitwise_and(quadro_pre_proces, quadro_pre_proces, mask=masc)
            cv.imshow("Debug Mode: Pre Processed quadro", quadro_pre_proces)
            cv.imshow("Debug Mode: Quadro Mascarado", quadro_mascarado)
        return geom_info