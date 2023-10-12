import math
import re

# Supongamos que el tamaño máximo de ventana es 16, entonces requiere de 4 bits; Tomaremos una de 4
VENTANA = 4
VENTANA_MAX_BITS = 4
def lecturaCadena():
    archivo = open("..\\datos\\texto.txt", 'r')
    cadena = archivo.readline()
    patron = r'[-,;._\s+]'

    # Vamos a tomar como delimitadores que separan subcadenas a los "espacios,_,-,punto y coma,punto")
    # limpiamos la cadena

    cadena_limpia = re.sub(patron, "", cadena)
    return cadena_limpia

def capturar_simbolos(cadena):
    simbolos = list()
    for s in cadena[0:]:
        if s not in simbolos:
            simbolos.append(s)
    return simbolos

def codigo_bloque(simbolos, bits_codigo):
    pseudo = list()
    # Aca le decimos que no tome "0b0" sino que omita 0b y quede con "0"
    # Además también queremos que el codigo sea de cierta longitud (000 por ej)
    pseudo.append(bin(0)[2:].zfill(bits_codigo))

    for i in range(1,len(simbolos)):
        pseudo.append(bin(i)[2:].zfill(bits_codigo))

    return pseudo

# Aca recibo la cadena de la misma longitud que la ventana, y me quedo con aquella con mayor prefijo que coincida
# con lo que se encuentra en la ventana
def match(cadena_ventana,cadena_no_comprimida):
    i=len(cadena_no_comprimida)
    cadena2=''.join(cadena_ventana)
    while i > 0:
        cadena1=cadena_no_comprimida[:i]
        if cadena2.find(cadena1) != -1:
            return cadena1
        else:
            i-=1
    return ''

def imprimirTabulaciones(ventana_lectura,contador):

    tabulaciones="\t"*contador
    print(tabulaciones + str(ventana_lectura))

def comprimir(cadena,pseudo_ascii,simbolos):
    ventana_lectura=[''] * VENTANA

    # Primero codificamos en 4 bits el valor "2" que es el tamaño de la ventana, porque el receptor debe saber
    # cual es el tamaño de ventana para luego decodificar
    comprimido = bin(VENTANA)[2:].zfill(VENTANA_MAX_BITS)

    # Llenamos la ventana y codificamos como si fueran coincidencias (Ya se encuentran los primeros 2 en la ventana)
    if len(ventana_lectura) < len(cadena):
        for i in range(len(ventana_lectura)):
            ventana_lectura[i]=cadena[i]
            simb = '1' + pseudo_ascii[simbolos.index(cadena[i])]
            comprimido = comprimido + simb
    else:
        return None

    print("\nTamaño de ventana + primeros \"n\" simbolos de la ventana: " + comprimido+"\n")

    si=len(ventana_lectura)

    contador=0
    while si < len(cadena):
        imprimirTabulaciones(ventana_lectura,contador)
        contador+=1

        # Tomamos el minimo porque puede que resten n simbolos < tamaño de la Ventana
        cadena_match = match(ventana_lectura,cadena[si : si + min(VENTANA,len(cadena)-si)])
        print("cadena que hizo match: " + str(cadena_match))

        if len(cadena_match) == 0 or len(cadena_match) == 1:
            for i in range(1,len(ventana_lectura)):
                ventana_lectura[i-1]=ventana_lectura[i]

            ventana_lectura[len(ventana_lectura)-1]=cadena[si]

            if len(cadena_match) == 0:
                # flag = 1 + codPseudo = (1 + long_codigo) bits
                simb = '1' + pseudo_ascii[simbolos.index(cadena[si])]

            else:
                simb = '0' + bin(ventana_lectura.index(cadena[si]))[2:].zfill(int(math.log2(VENTANA))) + bin(1)[2:].zfill(int(VENTANA))

            comprimido = comprimido + simb
            si += 1

        else:
            for i in range(len(cadena_match)):
                ventana_lectura[i] = ventana_lectura[VENTANA - len(cadena_match) +i]
                ventana_lectura[VENTANA - len(cadena_match) + i] = cadena[si+i]


            # flag = 0 + posicion_coincidencia = log2(ventana) + long_coincidencia (Como maximo es "tamaño de ventana")
            simb = '0' + bin(ventana_lectura.index(cadena[si]))[2:].zfill(int(math.log2(VENTANA))) + bin(len(cadena_match))[2:].zfill(int(VENTANA))
            comprimido = comprimido + simb
            si += len(cadena_match)

            """
            long_coincidencia = math.log2(len(cadena_match))
            if long_coincidencia % 2 == 0:
                simb = '0' + bin(ventana_lectura.index(cadena[si]))[2:].zfill(int(math.log2(VENTANA))) + bin(len(cadena_match))[2:].zfill(int(long_coincidencia))
            else:
                simb = '0' + bin(ventana_lectura.index(cadena[si]))[2:].zfill(int(math.log2(VENTANA))) + bin(len(cadena_match))[2:].zfill(int(long_coincidencia + 1))
            """

        """ if cadena[i] not in ventana_lectura:
            for i in range(1,len(ventana_lectura)):
                ventana_lectura[i-1]=ventana_lectura[i]

            ventana_lectura[len(ventana_lectura)-1]=cadena[i]

            # flag = 1 + codPseudo = (1 + long_codigo) bits
            simb = '1' + pseudo_ascii[simbolos.index(cadena[i])]
            comprimido = comprimido + simb
        else:
            for i in range(1,len(ventana_lectura)):
                ventana_lectura[i-1]=ventana_lectura[i]

            ventana_lectura[len(ventana_lectura)-1]=cadena[i]

            # flag = 0 + posicion_coincidencia = log2(ventana) + long_coincidencia = 1 bit (En este caso)
            simb = '0' + bin(ventana_lectura.index(cadena[i]))[2:].zfill(int (math.log2(VENTANA))) + '1'
            comprimido = comprimido + simb
            """

    imprimirTabulaciones(ventana_lectura,contador+1) # Ultima impresion
    return comprimido

def main():
    cadena = lecturaCadena()
    if cadena.strip() != '':
        simbolos = capturar_simbolos(cadena)
        if math.log2(len(simbolos)) % 2 != 0:
            li = int(math.log2(len(simbolos)) + 1)
        else:
            li = int(math.log2(len(simbolos)))

        pseudo_ascii = codigo_bloque(simbolos, li)
        for i in range(len(pseudo_ascii)):
            print("\""+simbolos[i]+"\" = "+pseudo_ascii[i])

        print(list(cadena))

        comprimido=comprimir(cadena,pseudo_ascii,simbolos)
        print("\n\nComprimido: "+comprimido)
        print("\n\nLongitud de Comprimido (Incluyendo 4 bits para tamaño de ventana): "+str(len(comprimido))+" bits")
        print("\n\nLongitud del original: "+str(len(cadena)*li)+" bits")

if __name__ == '__main__':
    main()
