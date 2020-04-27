import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
csfont = {'fontname': 'Times New Roman'}


def convertir_valores(preciosusd, preciosarg):
    listanueva = []
    for a, b in zip(preciosarg, preciosusd):
        one = float(a.replace(',', ''))
        second = float(b.replace(',', ''))
        listanueva.append(one/second)

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
    precio_gal_lista = convertir_valores(
        precio_gal_usd, precio_gal_arg)

    # lo di vuelta, ya que las fechas venian desde hoy hasta el pasado
    ccl = list(reversed(precio_gal_lista))
    # lista dos para calcular el aumento con respecto a la semana anterior
    ccl_1 = ccl[1:]
    # aumento con respecto a la semana anterior
    ccl_aumento = [ccl_1[i]/ccl[i] for i in range(len(ccl_1))]
    ccl_aumento.insert(0, 1.00)  # agrego la base 1 a la primer semana

    suma = aumentoporcentuales(ccl_aumento)
    porcentuales = ejeporcentuales(suma)

    return ccl_aumento, porcentuales


def agrega_anotacion(ax, porcentuales, num_sem, texto):
    x_ubicacion = porcentuales.index(num_sem)  # numero de semanas de gobierno
    y_ubicacion = num_sem
    ax.annotate(texto, xy=(x_ubicacion, y_ubicacion),
                xytext=(x_ubicacion-5, y_ubicacion-40), arrowprops=dict(arrowstyle="->"))


def main():
    precio_gal_arg_af = pd.read_csv('GGAL_ARG_AF_SEMANAL.csv', delimiter=",")['Último']
    precio_gal_usd_af = pd.read_csv('GGAL_USD_AF_SEMANAL.csv', delimiter=",")['Último']
    precio_gal_arg_mm = pd.read_csv('GGAL_ARG_MACRI_SEMANAL.csv', delimiter=',')['Último']
    precio_gal_usd_mm = pd.read_csv('GGAL_USD_MACRI_SEMANAL.csv', delimiter=',')['Último']

    ccl_af_aumento, porcentuales_af = procesa_datos(precio_gal_usd_af, precio_gal_arg_af)
    ccl_mm_aumento, porcentuales_mm = procesa_datos(precio_gal_usd_mm, precio_gal_arg_mm)

    plt.style.use('seaborn')
    ax = plt.subplot()

    agrega_anotacion(ax, porcentuales_mm, 200.54522782399653, 'JULIO-2019')
    agrega_anotacion(ax, porcentuales_mm, 16.76768621523337, 'DIC-2017')
    agrega_anotacion(ax, porcentuales_mm, 352.3990789015343, 'SEPT-2017')

    plt.rcParams["font.family"] = "Times New Roman"
    ax.plot(range(len(ccl_af_aumento)), porcentuales_af,
            color='cornflowerblue', label='Alberto Fernandez')
    ax.plot(range(len(ccl_mm_aumento)), porcentuales_mm,
            color='gold', label='Mauricio Macri')
    ax.set_xlabel('SEMANAS DE GOBIERNO', **csfont, fontsize=9)
    ax.set_ylabel('Δ PORCENTUAL', **csfont, fontsize=9)
    ax.set_title(
        "AUMENTO ACUMULADO CONTADO CON LIQUIDACIÓN \n en base a Grupo Galicia (GGAL)", **csfont)
    ax.margins(x=0)
    ax.set_ylim(ymin=-40)
    plt.legend(loc=4)
    plt.show()
    # plt.savefig('plot.png')


main()
