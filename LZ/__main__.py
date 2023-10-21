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
def imprimirTabulaciones(ventana_lectura,contador):

    tabulaciones="\t"*contador
    print(tabulaciones + str(ventana_lectura))
def comprimir():
    try:
        archivo = open(TXT, 'rb')
        ventana_lectura=[''] * VENTANA

        # Primero codificamos en 4 bits el valor "n < 16" que es el tamaño de la ventana, para que el receptor
        # luego pueda decodificar
        comprimido = bin(VENTANA)[2:].zfill(VENTANA_MAX_BITS)

        no_comprimido=codecs.decode(archivo.read(VENTANA),'utf-8')
        # Llenamos la ventana y la codificamos
        # Luego en la lectura sabremos n° de bits iniciales que solo expresan los codigos de los "simbolos"
        # cargados en la ventana, porque ya con los primeros bits sabemos el tamaño de la ventana, siendo un total
        # "log2(VENTANA)"
        if len(no_comprimido) == VENTANA:
            for i in range(VENTANA):
                ventana_lectura[i]=no_comprimido[i]
                simb = bin(ord(no_comprimido[i]))[2:]
                comprimido = comprimido + simb
        else:
            return ""

        print("\nTamaño de ventana + primeros \"n\" simbolos de la ventana: " + comprimido+"\n")

        contador=0
        long_fuente=VENTANA
        while True:
            imprimirTabulaciones(ventana_lectura,contador)
            #contador+=1

            aux = codecs.decode(archivo.read(1),'utf-8')
            if aux=='':
                break #Fin del archivo
            no_comprimido = aux #Se vuelve a inicializar al no comprimido cada vez que movemos la ventana
            cadena_match=""

            while len(match(ventana_lectura,no_comprimido))!=0 and len(no_comprimido) <= VENTANA:
                cadena_match=match(ventana_lectura,no_comprimido)
                aux = codecs.decode(archivo.read(1),'utf-8')
                if aux=='':
                    break #Fin del archivo
                no_comprimido=no_comprimido + aux

            long_fuente+=len(no_comprimido)

            # Quiere decir que hay coincidencia, aunque sea de longitud 1
            if(len(cadena_match) > 0):
                # flag = 0 + posicion_coincidencia expresada en log2(ventana) bits + long_coincidencia expresada en log2(ventana) + 1 bits
                simb = '0' + bin(ventana_lectura.index(cadena_match[0]))[2:].zfill(int(math.log2(VENTANA))) + bin(len(cadena_match))[2:].zfill(int(math.log2(VENTANA) + 1))

                if(len(cadena_match)==1):
                    for i in range(1,VENTANA):
                        ventana_lectura[i-1]=ventana_lectura[i]
                    ventana_lectura[VENTANA-1]=no_comprimido[0]
                else:
                    for i in range(len(cadena_match)):
                        ventana_lectura[i] = ventana_lectura[VENTANA - len(cadena_match)+i]
                        ventana_lectura[VENTANA - len(cadena_match) + i] = no_comprimido[i]
            else:
                # flag = 1 + codPseudo = (1 + long_codigo) bits
                simb = '1' + bin(ord(no_comprimido))[2:]
                for i in range(1,VENTANA):
                    ventana_lectura[i-1]=ventana_lectura[i]
                ventana_lectura[VENTANA-1]=no_comprimido[0]

            comprimido = comprimido + simb
            print("cadena que hizo match: " + cadena_match)

        imprimirTabulaciones(ventana_lectura,contador+1) # Ultima impresion
        print("\n\nLongitud del original: "+str(long_fuente*8)+" bits")

        return comprimido

    except FileNotFoundError:
        print(f"El archivo no se encontró.")
    except Exception as e:
        print(f"Se produjo un error: {str(e)}")
def main():
    comprimido = comprimir()
    if comprimido != "":
        print("\n\nComprimido: "+ comprimido)
        print("\n\nLongitud de Comprimido (Incluyendo 4 bits para tamaño de ventana): "+str(len(comprimido))+" bits")
    else:
        print("\n\nVENTANA DEMASIADO GRANDE PARA COMPRIMIR")

if __name__ == '__main__':
    main()
