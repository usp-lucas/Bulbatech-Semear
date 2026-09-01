"""
Ferramenta de Calibração e Teste de Visão.
Ajuste os Trackbars para encontrar o HSV ideal.
Aperte 's' para salvar.
Aperte 'q' para sair.
Quando apertado q e previamente tiver apertado 's':
Digite no terminar o nome do perfil salvo
"""
import numpy as np
import cv2 as cv
import json
import os
from aquisicao_img import FluxoVideo
from visao import PercepcaoVisual

class ConfiguradorDinamico:
    def __init__(self, endereco_config):
        self.fluxo_video = FluxoVideo()
        self.processador_img = PercepcaoVisual(debug=True)
        self.limites_hsv = {}
        self.rodando = True
        self.root = os.getcwd()
        self.endereco_config = os.path.join(self.root, endereco_config)
        self.limites_a_salvar = None
    def nothing(self,x):
        pass
    def prepara_interface(self):
        cv.namedWindow("Trackbars")
        janela_trackbars = "Trackbars"
        cv.createTrackbar("H_min",janela_trackbars,0,180,self.nothing)
        cv.createTrackbar("H_max",janela_trackbars,180,180,self.nothing)
        cv.createTrackbar("Sat_min",janela_trackbars,0,255,self.nothing)
        cv.createTrackbar("Sat_max",janela_trackbars,255,255,self.nothing)
        cv.createTrackbar("Val_min",janela_trackbars,0,255,self.nothing)
        cv.createTrackbar("Val_max",janela_trackbars,225,255,self.nothing)
    def executa_calibracao(self):
        self.fluxo_video.comeca()
        while self.rodando:
            quadro=self.fluxo_video.leia()
            h_min=cv.getTrackbarPos("H_min","Trackbars")
            h_max=cv.getTrackbarPos("H_max","Trackbars")
            sat_min=cv.getTrackbarPos("Sat_min","Trackbars")
            sat_max=cv.getTrackbarPos("Sat_max","Trackbars")
            val_min=cv.getTrackbarPos("Val_min","Trackbars")
            val_max=cv.getTrackbarPos("Val_max","Trackbars")
            self.processador_img.colors_hsv["CALIBRACAO"] = {
                "lower": np.array([h_min, sat_min, val_min], dtype=np.uint8),
                "upper": np.array([h_max, sat_max, val_max], dtype=np.uint8)
            }
            if quadro is not None:
                self.processador_img.canaliza_process(quadro, "CALIBRACAO")
            tecla = cv.waitKey(1) & 0xFF
            if tecla == ord('s'):
                self.limites_a_salvar = self.processador_img.colors_hsv.get("CALIBRACAO")
                print(f"Limites {self.limites_a_salvar} salvo com sucesso!")
            if tecla == ord('q') or tecla == 27:
                self.fluxo_video.pare()
                self.rodando = False
    def persista_dado(self):
        if self.limites_a_salvar is not None:
            val_calib_low = self.limites_a_salvar.get("lower")
            val_calib_upper = self.limites_a_salvar.get("upper")
            val_low_json = val_calib_low.tolist()
            val_upper_json = val_calib_upper.tolist()
            caminho_arq = self.endereco_config  
            try:
                with open(caminho_arq, 'r') as cfg:
                    calib_dict = json.load(cfg)
            except FileNotFoundError:
                calib_dict = {}
            nome_perfil = input("Digite um nome de perfil: ").strip().upper()
            calib_dict[nome_perfil] = {
                "lower": val_low_json,
                "upper": val_upper_json
            }
            with open(caminho_arq, 'w') as cfg:
                    json.dump(calib_dict, cfg, 
                        separators=(',', ':'), 
                        sort_keys=True, 
                        indent=4)
if __name__ == '__main__':
    calibracao = ConfiguradorDinamico(endereco_config="perfis.json")
    calibracao.prepara_interface()
    try:
        calibracao.executa_calibracao()
    except KeyboardInterrupt:
        print("Finalizando por interrupção via comando CTRL+C")
    except Exception as e:
        print(f"Erro inesperado: {e}. Encerrando...")
    finally:
        print("Encerrando sistema. Liberando câmera e destruindo janelas...")
        calibracao.persista_dado() 
        calibracao.fluxo_video.pare()
        cv.destroyAllWindows()    
        print("Sistema finalizado com sucesso.")