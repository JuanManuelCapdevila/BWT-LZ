import math
import re

# Supongamos que el tamaño máximo de ventana es 16, entonces requiere de 4 bits;
VENTANA = 4
VENTANA_MAX_BITS = 4
def lecturaCadena():
    archivo = open("../datos/texto1.txt", 'r')
    cadena = archivo.readline()
    patron = r'[-,;._\s+]'

    # limpiamos la cadena de "espacios,_,-,punto y coma,punto"
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
    pseudo.append(bin(0)[2:].zfill(bits_codigo))

    for i in range(1,len(simbolos)):
        pseudo.append(bin(i)[2:].zfill(bits_codigo))

    return pseudo

# Aca recibo la cadena de la misma longitud que la ventana, y me quedo con aquella con mayor prefijo que coincida
# con lo que se encuentra en la ventana
def match(cadena_ventana,cadena_no_comprimida):
    i=len(cadena_no_comprimida)
    cadena2=''.join(cadena_ventana)
    while i >= 0:
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

    # Primero codificamos en 4 bits el valor "n < 16" que es el tamaño de la ventana, para que el receptor
    # luego pueda decodificar
    comprimido = bin(VENTANA)[2:].zfill(VENTANA_MAX_BITS)

    # Llenamos la ventana y codificamos solo con el codigo de pseudo (porque inicialmente la ventana esta llena)
    # Luego en la lectura sabremos n° de bits iniciales que solo expresan los codigos de los "si"
    # cargados en la ventana, porque ya sabemos con los primeros bits el tamaño de la ventana, siendo un total
    # "log2(VENTANA)"
    if len(ventana_lectura) < len(cadena):
        for i in range(VENTANA):
            ventana_lectura[i]=cadena[i]
            simb = pseudo_ascii[simbolos.index(cadena[i])]
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
            if len(cadena_match) == 0:
                # flag = 1 + codPseudo = (1 + long_codigo) bits
                simb = '1' + pseudo_ascii[simbolos.index(cadena[si])]
            else:
                simb = '0' + bin(ventana_lectura.index(cadena[si]))[2:].zfill(int(math.log2(VENTANA))) + bin(1)[2:].zfill(int(VENTANA))

            for i in range(1,VENTANA):
                ventana_lectura[i-1]=ventana_lectura[i]

            ventana_lectura[VENTANA-1]=cadena[si]
            comprimido = comprimido + simb
            si += 1
        else:
            # flag = 0 + posicion_coincidencia expresada en log2(ventana) bits + long_coincidencia expresada en log2(ventana) bits
            simb = '0' + bin(ventana_lectura.index(cadena[si]))[2:].zfill(int(math.log2(VENTANA))) + bin(len(cadena_match))[2:].zfill(int(VENTANA))
            comprimido = comprimido + simb

            for i in range(len(cadena_match)):
                ventana_lectura[i] = ventana_lectura[VENTANA - len(cadena_match)+i]
                ventana_lectura[VENTANA - len(cadena_match) + i] = cadena[si+i]

            si += len(cadena_match)

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
