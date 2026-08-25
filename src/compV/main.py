import logging
import cv2
import sys
from percepcao.aquisicao_img import FluxoVideo
from percepcao.visao import PercepcaoVisual

ESC = 27

def configurar_logging():
    """Configura o sistema de logs para rastreabilidade em produção."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def main():

    logger = configurar_logging()
    logger.info("Iniciando sistema de visão robótica.")

    try:
        # Parâmetros centralizados para facilitar ajustes futuros
        RESOLUCAO = (640, 480)
        FPS = 30
        FONTE_CAMERA = 0  # 0 geralmente é a webcam integrada

        fluxo = FluxoVideo(
            resolucao=RESOLUCAO,
            taxaquadros=FPS,
            src=FONTE_CAMERA
        )
        logger.info(f"Câmera inicializada com resolução {RESOLUCAO}.")
    except Exception as e:
        logger.critical("Falha CRÍTICA ao acessar a câmera: %s", e, exc_info=True)
        return  


    fluxo.comeca()
    logger.info("Thread de captura de frames iniciada.")

    
    percepcao = PercepcaoVisual(debug=True)
    logger.info("Módulo de percepção visual instanciado.")

    
    ALVO_ATUAL = "SOL"
    logger.info(f"Alvo definido como: {ALVO_ATUAL}")

    
    rodando = True

    try:
        while rodando:
            frame = fluxo.leia()

            if frame is None or frame.size == 0:
                logger.warning("Frame inválido (None ou vazio). Aguardando...")
                cv2.waitKey(10)  # Pequena pausa para não sobrecarregar a CPU
                continue

            resultado = percepcao.canaliza_process(frame, ALVO_ATUAL)

            if "erro_pre_proces" in resultado:
                return logger.warning("Erro no pre-processamento, verifique a conexão da câmera. Quadro ignorado.")
            if resultado.get("alvo_confirmado"):
                coords = resultado["centroide"]
                area = resultado["area_cnt"]
                logger.debug(f"ALVO CONFIRMADO! Centro em {coords}, Área: {area:.2f}")
                # No futuro aplicar as coordenadas ao robô
            else:
                logger.debug("Nenhum alvo válido detectado neste frame.")

            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord('q') or tecla == ESC:
                logger.info("Comando de saída recebido pelo usuário.")
                rodando = False

    except KeyboardInterrupt:
        logger.info("Interrupção manual via Ctrl+C capturada.")
    except Exception as e:
        logger.critical("Erro inesperado no loop principal: %s", e, exc_info=True)
    finally:
        
        logger.info("Encerrando sistema. Liberando câmera e destruindo janelas...")
        fluxo.pare()               
        cv2.destroyAllWindows()    
        logger.info("Sistema finalizado com sucesso.")


if __name__ == "__main__":
    main()