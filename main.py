import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
csfont = {'fontname': 'Times New Roman'}

datos1 = pd.read_csv('GAL ARG AF ACTUAL.csv', delimiter=",")
datos2 = pd.read_csv('GAL USA AB ACTUAL.csv', delimiter=",")
precio_gal_usd_af = datos1['Último']
precio_gal_arg_af = datos2['Último']
precio_gal_lista_af = []


def convertir_valores(preciosusd, preciosarg, listanueva):
    for a, b in zip(preciosusd, preciosarg):
        one = float(a.replace(',', ''))
        second = float(b.replace(',', ''))
        listanueva.append(one/second)


convertir_valores(precio_gal_usd_af, precio_gal_arg_af, precio_gal_lista_af)

# lo di vuelta, ya que las fechas venian desde hoy hasta el pasado
ccl_af = list(reversed(precio_gal_lista_af))
# lista dos para calcular el aumento con respecto a la semana anterior
ccl_af_1 = ccl_af[1:]
# aumento con respecto a la semana anterior
ccl_af_aumento = [ccl_af_1[i]/ccl_af[i] for i in range(len(ccl_af_1))]
ccl_af_aumento.insert(0, 1.00)  # agrego la base 1 a la primer semana

suma = []


def aumentoporcentuales(aumento_ccl, suma):
    sum = 1
    for a in range(len(aumento_ccl)):
        sum *= aumento_ccl[a]
        suma.append(sum)


aumentoporcentuales(ccl_af_aumento, suma)

porcentuales_af = []


def ejeporcentuales(porcentuales, suma):
    for b in suma:  # para tener en el eje Y los porcentuales
        porcentuales.append((b - 1.00) * 100)


ejeporcentuales(porcentuales_af, suma)

# macri
datos3 = pd.read_csv('GGAL ARG MACRI SEMANAL .csv', delimiter=',')
datos4 = pd.read_csv('GGAL USD MACRI SEMANAL.csv', delimiter=',')
precio_gal_arg_mm = datos3['Último']
precio_gal_usd_mm = datos4['Último']
fechas_mm = datos4['Fecha']

precio_gal_lista_mm = []
convertir_valores(precio_gal_arg_mm, precio_gal_usd_mm, precio_gal_lista_mm)

# lo di vuelta, ya que las fechas venian desde hoy hasta el pasado
ccl_mm = list(reversed(precio_gal_lista_mm))
# lista dos para calcular el aumento con respecto a la semana anterior
ccl_mm_1 = ccl_mm[1:]
# aumento con respecto a la semana anterior
ccl_mm_aumento = [ccl_mm_1[i]/ccl_mm[i] for i in range(len(ccl_mm_1))]
ccl_mm_aumento.insert(0, 1.00)  # agrego la base 1 a la primer semana

suma1 = []

aumentoporcentuales(ccl_mm_aumento, suma1)
porcentuales_mm = []

ejeporcentuales(porcentuales_mm, suma1)

plt.style.use('seaborn')
ax = plt.subplot()

x_ubicacion = porcentuales_mm.index(
    200.54522782399653)  # numero de semanas de gobierno
y_ubicacion = 200.54522782399653
ax.annotate('JULIO-2019', xy=(x_ubicacion, y_ubicacion),
            xytext=(x_ubicacion-5, y_ubicacion-30), arrowprops=dict(arrowstyle="->"))

x_ubicacion2 = porcentuales_mm.index(
    16.76768621523337)  # numero de semanas de gobierno
y_ubicacion2 = 16.76768621523337

ax.annotate('DIC-2017', xy=(x_ubicacion2, y_ubicacion2),
            xytext=(x_ubicacion2-5, y_ubicacion2-40), arrowprops=dict(arrowstyle="->"))

x_ubicacion3 = porcentuales_mm.index(352.3990789015343)
y_ubicacion3 = 352.3990789015343
ax.annotate('SEPT-2017', xy=(x_ubicacion3, y_ubicacion3),
            xytext=(x_ubicacion3-5, y_ubicacion3-40), arrowprops=dict(arrowstyle="->"))

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
