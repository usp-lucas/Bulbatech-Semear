"""
Ferramenta de Calibração e Teste de Visão (Otimizada para RPi 4)
Ajuste os Trackbars para encontrar o HSV ideal.
Aperte 'q' para sair.
"""
import cv2 as cv
import numpy as np

def nothing(x):
    pass

# Inicializa a câmera
camera = cv.VideoCapture(1)

# Robustez: Tentativa de travar Auto-Exposure e Auto-White Balance
camera.set(cv.CAP_PROP_AUTO_EXPOSURE, 0.25)
camera.set(cv.CAP_PROP_AUTO_WB, 0)

# Configuração da Janela e Trackbars
cv.namedWindow("Trackbars")
cv.resizeWindow("Trackbars", 640, 300) # Janela de controle mais contida

# Valores iniciais de calibração (ajustáveis)
cv.createTrackbar("H Min", "Trackbars", 0, 180, nothing)
cv.createTrackbar("H Max", "Trackbars", 180, 180, nothing)
cv.createTrackbar("S Min", "Trackbars", 0, 255, nothing)
cv.createTrackbar("S Max", "Trackbars", 255, 255, nothing)
cv.createTrackbar("V Min", "Trackbars", 0, 255, nothing)
cv.createTrackbar("V Max", "Trackbars", 255, 255, nothing)

# Kernel retangular para morfologia otimizada para objetos retos e baixa resolução
kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))

while camera.isOpened():
    success, frame = camera.read()
    if not success:
        print("[ERRO] Não é possível acessar a câmera.")
        break
    
    # Otimização drástica: Resolução menor e interpolação barata para RPi 4
    quadro = cv.resize(frame, (320, 240), interpolation=cv.INTER_LINEAR)
    
    # Conversão para HSV (SEM o GaussianBlur prévio)
    frame_hsv = cv.cvtColor(quadro, cv.COLOR_BGR2HSV)
    
    # Captura os valores em tempo real
    hmin = cv.getTrackbarPos("H Min", "Trackbars")
    hmax = cv.getTrackbarPos("H Max", "Trackbars")    
    smin = cv.getTrackbarPos("S Min", "Trackbars")
    smax = cv.getTrackbarPos("S Max", "Trackbars")
    vmin = cv.getTrackbarPos("V Min", "Trackbars")
    vmax = cv.getTrackbarPos("V Max", "Trackbars")

    lower = np.array([hmin, smin, vmin])
    upper = np.array([hmax, smax, vmax])
    
    # Aplica a limiarização
    mask_crua = cv.inRange(frame_hsv, lower, upper)
    
    # Pós-processamento (Morfologia Matemática em substituição ao Blur)
    mask_limpa = cv.morphologyEx(mask_crua, cv.MORPH_OPEN, kernel)
    mask_limpa = cv.morphologyEx(mask_limpa, cv.MORPH_CLOSE, kernel)
    
    # Extração de Geometria a partir da máscara limpa
    contours, _ = cv.findContours(mask_limpa, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    # Textos de debug a serem sobrepostos no quadro final
    status_texto = "ALVO NAO ENCONTRADO"
    cor_texto = (0, 0, 255) # Vermelho
    
    if contours:
        cnt = max(contours, key=cv.contourArea)
        area = cv.contourArea(cnt)
        
        # Filtro de ruídos remanescentes via área
        if area > 100: # Valor baixo por causa da resolução 320x240
            
            # Cálculo de Solidez para validar se é um polígono sólido (cubo)
            hull = cv.convexHull(cnt)
            hull_area = cv.contourArea(hull)
            
            if hull_area > 0:
                solidez = area / float(hull_area)
                
                # Validação completa: Tem área significativa e solidez adequada
                if solidez > 0.85:
                    status_texto = f"ALVO DETECTADO | Area: {int(area)}"
                    cor_texto = (0, 255, 0) # Verde
                    
                    # Desenha a Bounding Box do objeto detectado
                    x, y, w, h = cv.boundingRect(cnt)
                    cv.rectangle(quadro, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    
                    # Calcula e desenha o Centroide
                    M = cv.moments(cnt)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        cv.circle(quadro, (cx, cy), 5, (0, 0, 255), -1)

    # Exibição dos arrays no próprio vídeo, poupando I/O do terminal
    cv.putText(quadro, status_texto, (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.4, cor_texto, 1)
    cv.putText(quadro, f"Low : {lower}", (10, 210), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    cv.putText(quadro, f"High: {upper}", (10, 230), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # Mostra os resultados. 
    # Compare a 'Mascara Crua' com a 'Mascara Limpa' para ver o poder da Morfologia
    cv.imshow("Quadro Original com Deteccao", quadro)
    cv.imshow("Mascara Crua (Sem Morfologia)", mask_crua)
    cv.imshow("Mascara Limpa (Pronta para Roteamento)", mask_limpa)
    
    # Finaliza ao pressionar a tecla 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv.destroyAllWindows()