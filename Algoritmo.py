import cv2


import easyocr

#medimos el tiempo de ejecucion para los fps----------
reader = easyocr.Reader(["es","en"], gpu = True)



placa = []
image = cv2.imread("a1.jpg",1)
#cv2.imshow('placaIn', image)
#cambio de color a una escala de grises, y difeminamos
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.blur(gray, (3,3))
#cv2.imshow('placagray', gray)

#con canny definimos los bordes de la imagen
canny = cv2.Canny(gray,150,200)
#cv2.imshow('placaCanny', canny)
canny = cv2.dilate(canny, None,iterations=1)
#cv2.imshow('placaDilate', canny)

# con cv2.RETR_LIST, buscamos contornos
cnts,_=cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
# desecho de contornos con for
for c in cnts:
    # extraemos el area del contorno
    area = cv2.contourArea(c)
    #Buscamos un contorno especifico
    х,у,w,h = cv2.boundingRect(c)
    # Calculamos el perímetro del contorno
    epsilon = 0.09*cv2.arcLength(c, True)
    # aproximamos el contorno a un cuadrado
    approx = cv2.approxPolyDP (c, epsilon, True)
    # Buscamos un contorno con 4 vertices
    if len(approx)==4 and area>9000:
        #print('area=', area)
        ##cv2.drawContours (image, [c],e, (e,255,0), 2)

        # Verificamos la relacion de aspecto de ancho y altura
        aspect_ratio = float(w)/h
        if aspect_ratio>2.0:
            # Recorte de la placa
            placa = gray[у:у+h,х:х+w]
            #cv2.imshow('placarec', placa)




            # con pytesseract, extraemos los caracteres dentro de placa
            reader = reader.readtext(placa)
            #print('reader=', reader)
            tex = reader[0]
            text = tex[1]
            #text=pytesseract.image_to_string(placa, config='--psm 10 tessedit_char_whitelist=0123456789')
            #text=pytesseract.image_to_string(placa, config='--psm 7')
            print('text=', text)
            
            cv2.imshow('placa', placa)
            cv2.moveWindow('placa',780,10)

            #sobreponemos a la imagen el valor de la placa
            cv2.rectangle(image,(х,у),(х+w,у+h),(0,255,0),3)
            #cv2.putText(image, text, (х-20,у-10),1,2.2, (0,255,0),3)
            #patron = re.compile('[a-zA-Z]{3}-[0-9]{3}')
            #print(patron)

cv2.imshow('Image', image)
cv2.imshow('Canny', canny)
cv2.moveWindow('Image',45,10)
cv2.waitKey(0)
