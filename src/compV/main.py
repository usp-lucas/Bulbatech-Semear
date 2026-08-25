import logging
import cv2
import sys
from percepcao.aquisicao_img import VideoStream
from percepcao.visao import PercepcaoVisual


def configurar_logging():
    """Configura o sistema de logs para rastreabilidade em produção."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def main():
    # 1. Inicialização com Logs
    logger = configurar_logging()
    logger.info("Iniciando sistema de visão robótica.")

    # 2. Instanciação Defensiva (bloco try/except)
    try:
        # Parâmetros centralizados para facilitar ajustes futuros
        RESOLUCAO = (640, 480)
        FPS = 30
        FONTE_CAMERA = 0  # 0 geralmente é a webcam integrada

        stream = VideoStream(
            resolucao=RESOLUCAO,
            taxaquadros=FPS,
            src=FONTE_CAMERA
        )
        logger.info(f"Câmera inicializada com resolução {RESOLUCAO}.")
    except Exception as e:
        logger.critical("Falha CRÍTICA ao acessar a câmera: %s", e, exc_info=True)
        return  # Sai do programa se não houver câmera

    # 3. Início da Thread de captura (módulo de aquisição)
    stream.comeca()
    logger.info("Thread de captura de frames iniciada.")

    # 4. Instanciação do Módulo de Visão
    # Defina debug=True para ver os círculos/retângulos (modo didático)
    percepcao = PercepcaoVisual(debug=True)
    logger.info("Módulo de percepção visual instanciado.")

    # 5. Configuração do alvo (pode ser "SOL" ou "NUVEM")
    ALVO_ATUAL = "SOL"
    logger.info(f"Alvo definido como: {ALVO_ATUAL}")

    # 6. Controle do loop principal
    rodando = True

    try:
        while rodando:
            # --- AQUISIÇÃO DEFENSIVA ---
            frame = stream.leia()

            # Verifica se o frame é válido (não pode ser None nem vazio)
            if frame is None or frame.size == 0:
                logger.warning("Frame inválido (None ou vazio). Aguardando...")
                cv2.waitKey(10)  # Pequena pausa para não sobrecarregar a CPU
                continue

            # --- PROCESSAMENTO (chamada ao módulo de visão) ---
            resultado = percepcao.canaliza_process(frame, ALVO_ATUAL)

            # --- LOG ESTRATÉGICO (rastreabilidade) ---
            if "erro_pre_proces" in resultado:
                return logger.warning("Erro no pre-processamento, verifique a conexão da câmera. Quadro ignorado.")
            if resultado.get("alvo_confirmado"):
                coords = resultado["centroide"]
                area = resultado["area_cnt"]
                logger.debug(f"ALVO CONFIRMADO! Centro em {coords}, Área: {area:.2f}")
                # Aqui no futuro você poderia publicar essas coordenadas para o robô
            else:
                logger.debug("Nenhum alvo válido detectado neste frame.")

            # --- CONTROLE DE SAÍDA (tecla 'q' ou ESC) ---
            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord('q') or tecla == 27:  # 27 = ESC
                logger.info("Comando de saída recebido pelo usuário.")
                rodando = False

    except KeyboardInterrupt:
        logger.info("Interrupção manual via Ctrl+C capturada.")
    except Exception as e:
        # Captura qualquer erro inesperado no loop para não travar o robô
        logger.critical("Erro inesperado no loop principal: %s", e, exc_info=True)
    finally:
        # --- FINALIZAÇÃO OBRIGATÓRIA (libera recursos) ---
        logger.info("Encerrando sistema. Liberando câmera e destruindo janelas...")
        stream.pare()               # Para a thread de captura
        cv2.destroyAllWindows()    # Fecha todas as janelas OpenCV abertas
        logger.info("Sistema finalizado com sucesso.")


if __name__ == "__main__":
    main()