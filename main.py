import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
csfont = {'fontname': 'Times New Roman'}

def convertir_valores(preciosusd, preciosarg):
    listanueva = []
    for a, b in zip(preciosarg, preciosusd):
        listanueva.append(a*10/b)
    listanueva= [x for x in listanueva if (np.isnan(x) == False)]
    return listanueva

def aumentoporcentuales(aumento_ccl):
    suma = []
    sum = 1
    for a in range(len(aumento_ccl)):
        sum *= aumento_ccl[a]
        suma.append(sum)
    return suma

def ejeporcentuales(suma):
    porcentuales = []
    for b in suma:  # para tener en el eje Y los porcentuales
        porcentuales.append((b - 1.00) * 100)

    return porcentuales

def procesa_datos(precio_gal_usd, precio_gal_arg):

    precio_gal_lista = convertir_valores(precio_gal_usd, precio_gal_arg)

    # lista dos para calcular el aumento con respecto a la semana anterior
    precio_gal_lista2 = precio_gal_lista[1:]
    # aumento con respecto a la semana anterior
    ccl_aumento = [precio_gal_lista2[i]/precio_gal_lista[i] for i in range(len(precio_gal_lista2))]
    ccl_aumento.insert(0, 1.00)  # agrego la base 1 a la primer semana

    suma = aumentoporcentuales(ccl_aumento)
    porcentuales = ejeporcentuales(suma)
    print(porcentuales)
    return ccl_aumento, porcentuales

def agrega_anotacion(ax, porcentuales, num_sem, texto):
    x_ubicacion = porcentuales.index(num_sem)  # numero de semanas de gobierno
    y_ubicacion = num_sem
    ax.annotate(texto, xy=(x_ubicacion, y_ubicacion), xytext=(x_ubicacion-5, y_ubicacion-40), arrowprops=dict(arrowstyle="->"))

def main():
    ggal_arg_macri = yf.Ticker('GGAL.BA').history(start='2015-12-10', end='2019-12-10', interval='1wk')
    ggal_usd_macri = yf.Ticker('GGAL').history(start='2015-12-10', end='2019-12-10', interval='1wk')
    ggal_arg_af = yf.Ticker('GGAL.BA').history(start='2019-12-10', end='2020-04-27', interval='1wk')
    ggal_usd_af = yf.Ticker('GGAL').history(start='2019-12-10', end='2020-04-27', interval='1wk')

    precio_arg_mm = ggal_arg_macri['Close'].values.tolist()
    precio_usd_mm = ggal_usd_macri['Close'].values.tolist()
    precio_arg_af = ggal_arg_af['Close'].values.tolist()
    precio_usd_af = ggal_usd_af['Close'].values.tolist()

    ccl_mm_aumento, porcentuales_mm = procesa_datos(precio_usd_mm, precio_arg_mm)
    ccl_af_aumento, porcentuales_af = procesa_datos(precio_usd_af, precio_arg_af)

    plt.style.use('seaborn')
    ax = plt.subplot()

    agrega_anotacion(ax, porcentuales_mm,180.87213928484042, 'JULIO-2019')
    agrega_anotacion(ax, porcentuales_mm,10.150265391274637, 'DIC-2017')
    agrega_anotacion(ax, porcentuales_mm,323.27022675589745, 'SEPT-2017')

    plt.rcParams["font.family"] = "Times New Roman"
    ax.plot(range(len(ccl_mm_aumento)), porcentuales_mm, color='gold', label='Mauricio Macri')
    ax.plot(range(len(ccl_af_aumento)), porcentuales_af, color='cornflowerblue', label='Alberto Fernandez')
    ax.set_xlabel('SEMANAS DE GOBIERNO', **csfont, fontsize=9)
    ax.set_ylabel('Δ PORCENTUAL', **csfont, fontsize=9)
    ax.set_title("AUMENTO ACUMULADO CONTADO CON LIQUIDACIÓN \n en base a Grupo Galicia (GGAL)", **csfont)
    ax.margins(x=0)
    ax.set_ylim(ymin=-40)
    plt.legend(loc=4)
    plt.show()
    # plt.savefig('plot.png')
main()
