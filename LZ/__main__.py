import math
import codecs
# Supongamos que el tamaño máximo de ventana es 16, entonces requiere de 4 bits;
VENTANA = 4
VENTANA_MAX_BITS = 4
TXT = "../datos/texto1.txt"

def match(cadena_ventana,cadena_no_comprimida):
    cadena1=''.join(cadena_ventana)
    if cadena1.find(cadena_no_comprimida) != -1:
        return cadena_no_comprimida

    return ''
def comprimido_bytes(comprimido_bin):
    while len(comprimido_bin) % 8 != 0:
        comprimido_bin = comprimido_bin + '0'

    arr_bytes=bytes([int(comprimido_bin[i:i+8], 2) for i in range(0, len(comprimido_bin), 8)])
    return arr_bytes

def movimiento_ventana(ventana_lectura,procesado,long_match,pos_byte):
    if(long_match > 1):
        if(long_match!=VENTANA): #Si la coincidencia es toda la ventana, entonces no se cambia
            for i in range(long_match,VENTANA):
                ventana_lectura[i - long_match]=ventana_lectura[i]
            for i in range(long_match):
                ventana_lectura[VENTANA - long_match + i] = procesado[pos_byte + i]
    else:
        for i in range(1,VENTANA):
            ventana_lectura[i-1]=ventana_lectura[i]
        ventana_lectura[VENTANA-1]=procesado[pos_byte]

    return ventana_lectura

def comprimir():
    try:
        archivo = open(TXT, 'rb')
        ventana_lectura=[''] * VENTANA

        # Primero codificamos en 4 bits el valor "n < 16" que es el tamaño de la ventana, para que el receptor
        # luego pueda decodificar
        comprimido = bin(VENTANA)[2:].zfill(VENTANA_MAX_BITS)
        procesado=codecs.decode(archivo.read(VENTANA),'utf-8')
        # Llenamos la ventana y la codificamos
        # Luego en la lectura sabremos n° de bits iniciales que solo expresan los codigos de los "simbolos"
        # cargados en la ventana, porque ya con los primeros bits sabemos el tamaño de la ventana, siendo un total
        # "log2(VENTANA)"
        if not procesado:
            return "" #Fin del archivo
        else:
            for i in range(VENTANA):
                ventana_lectura[i]=procesado[i]
                simb = bin(ord(procesado[i]))[2:]
                comprimido = comprimido + simb

        print("\nTamaño de ventana + primeros \"n\" simbolos de la ventana: " + comprimido+"\n")

        long_fuente=VENTANA
        aux = archivo.read(1)
        if not aux:
            return "" #Fin del archivo
        procesado += chr(ord(aux))
        pos_byte=VENTANA

        while True:
            print(str(ventana_lectura))

            cadena_match=""

            while len(match(ventana_lectura,procesado[pos_byte:]))!=0 and len(cadena_match) < VENTANA:
                cadena_match=match(ventana_lectura,procesado[pos_byte:])
                aux = archivo.read(1)
                if not aux:
                    break #Fin del archivo
                procesado += chr(ord(aux))

            # Quiere decir que hay coincidencia, aunque sea de longitud 1
            if(len(cadena_match) > 0):

                # flag = 0 + posicion_coincidencia expresada en log2(ventana) bits + long_coincidencia expresada en log2(ventana) + 1 bits
                simb = '0' + bin(ventana_lectura.index(cadena_match[0]))[2:].zfill(int(math.log2(VENTANA))) + bin(len(cadena_match))[2:].zfill(int(math.log2(VENTANA) + 1))
                ventana_lectura=movimiento_ventana(ventana_lectura,procesado,len(cadena_match),pos_byte)
                pos_byte+= len(cadena_match)
            else:
                #Si no coincide le sumo 1 a pos_byte, si hay coincidencia le sumo len(cadena_match) entonces siempre apunta
                #al siguiente de la ventana, es decir, el ultimo procesado
                aux = archivo.read(1)
                if not aux:
                    break #Fin del archivo
                procesado += chr(ord(aux))

                # flag = 1 + codPseudo = (1 + long_codigo) bits
                simb = '1' + bin(ord(procesado[pos_byte]))[2:]
                ventana_lectura=movimiento_ventana(ventana_lectura,procesado,len(cadena_match),pos_byte)
                pos_byte+= 1

            comprimido = comprimido + simb
            print("cadena que hizo match: " + cadena_match)

        long_fuente=pos_byte
        print("\n\nLongitud del original: "+str(long_fuente*8)+" bits")

        return comprimido_bytes(comprimido)

    except FileNotFoundError:
        print(f"El archivo no se encontró.")
    except Exception as e:
        print(f"Se produjo un error: {str(e)}")
def main():
    comprimido = comprimir()
    if comprimido != "":
        print("\n\nComprimido (Bytes): "+ str(comprimido))
        print("\n\nLongitud de Comprimido (Incluyendo 4 bits para tamaño de ventana): "+str(len(comprimido)*8)+" bits")
    else:
        print("\n\nVENTANA DEMASIADO GRANDE PARA COMPRIMIR")

if __name__ == '__main__':
    main()