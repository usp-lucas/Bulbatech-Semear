"""
Ferramenta de Calibração e Teste de Visão.
Ajuste os Trackbars para encontrar o HSV ideal.
Aperte 'q' para sair.
"""
import cv2 as cv
import numpy as np

def nothing(x):
    pass


camera = cv.VideoCapture(0)

camera.set(cv.CAP_PROP_AUTO_EXPOSURE, 0.25)
camera.set(cv.CAP_PROP_AUTO_WB, 0)

cv.namedWindow("Trackbars")
cv.resizeWindow("Trackbars", 640, 300)


cv.createTrackbar("H Min", "Trackbars", 0, 180, nothing)
cv.createTrackbar("H Max", "Trackbars", 180, 180, nothing)
cv.createTrackbar("S Min", "Trackbars", 0, 255, nothing)
cv.createTrackbar("S Max", "Trackbars", 255, 255, nothing)
cv.createTrackbar("V Min", "Trackbars", 0, 255, nothing)
cv.createTrackbar("V Max", "Trackbars", 255, 255, nothing)

kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))

while camera.isOpened():
    success, frame = camera.read()
    if not success:
        print("[ERRO] Não é possível acessar a câmera.")
        break
    
    
    quadro = cv.resize(frame, (320, 240), interpolation=cv.INTER_LINEAR)
    
    frame_hsv = cv.cvtColor(quadro, cv.COLOR_BGR2HSV)


    hmin = cv.getTrackbarPos("H Min", "Trackbars")
    hmax = cv.getTrackbarPos("H Max", "Trackbars")    
    smin = cv.getTrackbarPos("S Min", "Trackbars")
    smax = cv.getTrackbarPos("S Max", "Trackbars")
    vmin = cv.getTrackbarPos("V Min", "Trackbars")
    vmax = cv.getTrackbarPos("V Max", "Trackbars")

    lower = np.array([hmin, smin, vmin])
    upper = np.array([hmax, smax, vmax])
    
    
    mask_crua = cv.inRange(frame_hsv, lower, upper)
    
    
    mask_limpa = cv.morphologyEx(mask_crua, cv.MORPH_OPEN, kernel)
    mask_limpa = cv.morphologyEx(mask_limpa, cv.MORPH_CLOSE, kernel)
    
    
    contours, _ = cv.findContours(mask_limpa, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    
    status_texto = "ALVO NAO ENCONTRADO"
    cor_texto_vermelho = (0, 0, 255) 
    
    if contours:
        cnt = max(contours, key=cv.contourArea)
        area = cv.contourArea(cnt)
        
        
        if area > 100: # Valor baixo por causa da resolução 320x240
            
            
            hull = cv.convexHull(cnt)
            hull_area = cv.contourArea(hull)
            
            if hull_area > 0:
                solidez = area / float(hull_area)
                
                
                if solidez > 0.85:
                    status_texto = f"ALVO DETECTADO | Area: {int(area)}"
                    cor_texto_verde = (0, 255, 0)
                    
                    
                    x, y, w, h = cv.boundingRect(cnt)
                    cv.rectangle(quadro, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    
                    
                    M = cv.moments(cnt)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        cv.circle(quadro, (cx, cy), 5, (0, 0, 255), -1)

    
    cv.putText(quadro, status_texto, (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.4, cor_texto_verde, 1)
    cv.putText(quadro, f"Low : {lower}", (10, 210), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    cv.putText(quadro, f"High: {upper}", (10, 230), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    cv.imshow("Quadro Original com Deteccao", quadro)
    cv.imshow("Mascara Crua (Sem Morfologia)", mask_crua)
    cv.imshow("Mascara Limpa (Pronta para Roteamento)", mask_limpa)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv.destroyAllWindows()