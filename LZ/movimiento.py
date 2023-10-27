from variables_globales import VENTANA
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