import math
from variables_globales import VENTANA_MAX_BITS
from movimiento import movimiento_ventana
def descomprimir(comprimido):

    procesado=bin(comprimido[0])[2:].zfill(8)
    n_byte=1

    if(VENTANA_MAX_BITS > 8):
        i=8
        while i < VENTANA_MAX_BITS:
            procesado += bin(comprimido[n_byte])[2:].zfill(8)
            i+=8
            n_byte+=1

    tam_ventana=int(procesado[:VENTANA_MAX_BITS],2)
    pos_bit=VENTANA_MAX_BITS #posicion del primer bit del comprimido

    ventana=bytearray()
    descomprimido=bytearray()

    while(len(ventana) < tam_ventana):
        procesado += bin(comprimido[n_byte])[2:].zfill(8)
        byte=int(procesado[pos_bit:pos_bit+8],2).to_bytes(1,byteorder='big')
        descomprimido.append(byte[0])
        ventana.append(byte[0])
        pos_bit+=8
        n_byte+=1

    """
    Cuando enviamos como "bytes" al comprimido, este se rellena con 0s al final para que podamos hacer un n°
    entero de lecturas de 8 bits; todo esto es porque los primeros "VENTANA_MAX" bits nos indican el tamaño de 
    ventana utilizada en la compresion, que puede ser 1 byte, menos o más de 1 byte.
    Sabiendo cuantos bits son, podemos determinar cuantos bits tenemos de relleno para completar el ultimo byte
    """
    while n_byte < len(comprimido):
        if(pos_bit < len(procesado)):
            #Si hay un 1, entonces lo que sigue son 8 bits de un símbolo que no existe en la ventana
            if(procesado[pos_bit] == '1'):
                pos_bit+=1

                if(len(procesado[pos_bit:]) < 8): #Se cumple cuando necesito procesar mas bits para decodificar
                    procesado += bin(comprimido[n_byte])[2:].zfill(8)
                    n_byte+=1 #Siempre apunta al siguiente byte por leer

                byte=int(procesado[pos_bit:pos_bit+8],2).to_bytes(1,byteorder='big')
                ventana=movimiento_ventana(ventana,byte,len(byte),0) #(pos_bit/8) es la posicion del ultimo byte procesado
                descomprimido.append(byte[0])
                pos_bit+=8

            else:
                pos_bit+=1
                #Si la cantidad de bits que necesito leer son menores o iguales a los que restan, puedo leer
                if pos_bit + int(math.log2(tam_ventana))*2 + 1 <= len(comprimido)*8:
                    while len(procesado[pos_bit:]) < int(math.log2(tam_ventana))*2 + 1:
                        procesado += bin(comprimido[n_byte])[2:].zfill(8)
                        n_byte+=1
                else:
                    break

                binario = procesado[pos_bit:pos_bit + (int(math.log2(tam_ventana))*2 + 1)]
                pos_coincidencia=int(binario[:int(math.log2(tam_ventana))],2)
                long_coincidencia=int(binario[int(math.log2(tam_ventana)):int(math.log2(tam_ventana))*2 + 1],2)
                bytes=ventana[pos_coincidencia:pos_coincidencia+long_coincidencia]
                ventana=movimiento_ventana(ventana,bytes,len(bytes),0)
                descomprimido.extend(bytes)
                pos_bit+= (int(math.log2(tam_ventana))*2 + 1)

        else:
            procesado += bin(comprimido[n_byte])[2:].zfill(8)
            n_byte+=1

#Llegamos al ultimo byte, adonde estan los bits de relleno en el comprimido.. Aca se puede presentar la
#situacion en la que estemos trabajando con una ventana de tamaño 2 o 4, y el flag, la posicion de coincidencia
#y longitud de coincidencia requieran de 6 bits para el caso de la de tamaño 4. También sabemos que en el peor
#caso se requieran de 7 bits de relleno, por lo tanto tendremos que hacer una ultima decodificacion si es
#necesario

    if(pos_bit < len(comprimido)*8 and procesado[pos_bit] != '1'):
        pos_bit+=1
        if(len(procesado[pos_bit:]) >= int(math.log2(tam_ventana)) *2 + 1):
            binario = procesado[pos_bit:pos_bit + (int(math.log2(tam_ventana))*2 + 1)]
            long_coincidencia=int(binario[int(math.log2(tam_ventana)):int(math.log2(tam_ventana))*2 + 1],2)

            if(long_coincidencia!=0):
                pos_coincidencia=int(binario[:int(math.log2(tam_ventana))],2)
                bytes=ventana[pos_coincidencia:pos_coincidencia+long_coincidencia]
                ventana=movimiento_ventana(ventana,bytes,len(bytes),0)
                descomprimido.extend(bytes)

    return descomprimido


