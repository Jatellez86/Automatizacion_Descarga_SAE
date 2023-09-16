# Importa las bibliotecas necesarias para la automatización del navegador con Selenium
# **********************************************************************************************
#  @Nombre: Boot descarga datos GetsSae
#  @Autor: Javier Tellez
#  @Fecha: 20230315
#  @Cambios:
#  @Ayudas:
# **********************************************************************************************
#----------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time 
import os
import shutil
from datetime import date
from datetime import datetime, timedelta
import pandas as pd                                   


# Definicion de variables ---------------------------------------------------------------------
driver = False
session_id = False
loginState = False
user = 'user_prueba'
password = 'pwd_prueba'
fecha_actual = date.today()
fecha_anterior = fecha_actual - timedelta(days=1)

# lista de dias para recorrer-------------------------------------------------------------------

# Crear un objeto datetime para el primer día del año 2023 o cualquier otro
fecha = datetime(2023, 1, 1)

# Crear una lista para almacenar los días del año
dias_del_anio = []

# Obtener la fecha de ayer
ayer = datetime.now() - timedelta(days=1)

# Iterar sobre los días restantes del año o rango de fechas hasta ayer
while fecha <= ayer:
    dias_del_anio.append(fecha.strftime("%d/%m/%Y"))
    fecha += timedelta(days=1)

date_calendar = pd.DataFrame({'date': dias_del_anio})
date_calendar["date"] = pd.to_datetime(date_calendar["date"], format='%d/%m/%Y')

# lista de fechas en el directorio ------------------------------------------------------------

ruta = 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\12 inoperables'

archivos = [archivo for archivo in os.listdir(ruta) if 'UF17.csv' in archivo]  # Obtener la lista de archivos en la ruta especificada

filenames = []
dates = []


# Recorrer la lista de archivos y extraer la fecha y el nombre del archivo
for archivo in archivos:
    fecha = archivo[:8]  # Los primeros 8 caracteres del nombre del archivo corresponden a la fecha
    filenames.append(archivo)
    dates.append(pd.to_datetime(fecha, format='%Y%m%d').strftime('%d/%m/%Y'))  # Convertir la fecha al formato deseado

# Crear el DataFrame con la información obtenida
df_alejandria_uf06 = pd.DataFrame({'date': dates, 'filename': filenames})
df_alejandria_uf06["date"] = pd.to_datetime(df_alejandria_uf06["date"], format='%d/%m/%Y')

# Hacer la unión de los dos DataFrames por la columna "date"
directory_ready_uf06 = pd.merge(date_calendar, df_alejandria_uf06, on='date', how='left')

# Filtrar las fechas que están en date_calendar
df_filtrado_uf06 = directory_ready_uf06[directory_ready_uf06['filename'].isna()]
df_filtrado_uf06['date'] = pd.to_datetime(df_filtrado_uf06['date']).dt.strftime('%d/%m/%Y')


for i in df_filtrado_uf06['date']:
    print(i)


#print(df_filtrado_uf06)

#driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
chromedriver = 'chromedriver.exe'

# Características en el Web Driver ------------------------------------------------------------
session_id = False
loginState = False
driver = False
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Functions -----------------------------------------------------------------------------------
def openBrowser():
    global session_id
    global loginState
    global driver    
    try:
        if session_id == False:        
            driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
            driver.implicitly_wait(40)  # seconds
            driver.maximize_window()
            session_id = driver.session_id
        return True
    except Exception as e: 
        print(str(e))
        return False

# Logic --------------------------------------------------------------------------------
openBrowser()

# pagina principal de gets sae zmo III
driver.get('http://10.50.128.91/GestSAE/Account/Login.aspx?ReturnUrl=%2fGestSAE%2fDefault.aspx')
time.sleep(1)

# enviar llaves de usuario y contraseña

driver.find_element('id','ctl00_MainContent_LoginUser_UserName').send_keys(user)
time.sleep(1)
driver.find_element('id','ctl00_MainContent_LoginUser_Password').send_keys(password)
time.sleep(1)
driver.find_element('xpath','//*[@id="ctl00_MainContent_LoginUser_LoginButton"]').click()
time.sleep(1)
driver.refresh()

#ciclo que recorre dias
for i in df_filtrado_uf06['date']:

    # Define la ruta del directorio donde se encuentran los archivos
    directorio = "C:\\Users\\javier.tellez\\Downloads"

    # Obtiene una lista con todos los archivos del directorio
    archivos = os.listdir(directorio)

    # Recorre la lista de archivos y elimina cada uno de ellos
    for archivo in archivos:
        ruta_archivo = os.path.join(directorio, archivo)
        os.remove(ruta_archivo)

    # descarga de inoperables
    fecha = datetime.strptime(i, "%d/%m/%Y")
    dia_ajus = fecha.strftime("%Y%m%d")

    inoper_1 = '01/01/2022 00:00'
    inoper_2 = '31/12/2024 23:59'

    driver.get("http://10.50.128.91/GestSAE/Informes/CondInoperablesEmpresa.aspx")
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_dateInicio_dateInput').send_keys(inoper_1)
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_dateFin_dateInput').send_keys(inoper_2)
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_btnver').click()
    time.sleep(2)
    driver.get("http://10.50.128.91/GestSAE/Informes/VisorInformes.aspx")
    time.sleep(25)
    driver.find_element('id','ReportViewer1_ctl01_ctl05_ctl00').send_keys('CSV (delimitado por comas)')
    time.sleep(1)
    driver.find_element('id','ReportViewer1_ctl01_ctl05_ctl01').click()
    time.sleep(1)
    driver.refresh()

    # descarga accidentes de transito

    #accident_day = str(date.today()- timedelta(days=1))

    driver.get("http://10.50.128.91/GestSAE/Informes/AccDetalleEventosTransito.aspx")
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_dateInicio_dateInput').send_keys(i)
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_dateFin_dateInput').send_keys(i)
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_chkTabla').click()
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_btnver').click()
    time.sleep(1)
    driver.get("http://10.50.128.91/GestSAE/Informes/VisorInformes.aspx")
    time.sleep(25)
    driver.find_element('id','ReportViewer1_ctl01_ctl05_ctl00').send_keys('CSV (delimitado por comas)')
    time.sleep(2)
    driver.find_element('id','ReportViewer1_ctl01_ctl05_ctl01').click()
    time.sleep(1)
    driver.refresh()

    # descarga accidentes de transito estacion

    driver.get("http://10.50.128.91/GestSAE/Informes/AccDetalleEventosEstacion.aspx")
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_dateInicio_dateInput').send_keys(i)
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_dateFin_dateInput').send_keys(i)
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_chkTabla').click()
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_btnver').click()
    time.sleep(1)
    driver.get("http://10.50.128.91/GestSAE/Informes/VisorInformes.aspx")
    time.sleep(2)
    driver.find_element('id','ReportViewer1_ctl01_ctl05_ctl00').send_keys('CSV (delimitado por comas)')
    time.sleep(2)
    driver.find_element('id','ReportViewer1_ctl01_ctl05_ctl01').click()
    time.sleep(1)
    driver.refresh()

    # descarga novedades de seguridad y convivencia

    driver.get("http://10.50.128.91/GestSAE/Informes/AccDetalleEventosConvivencia.aspx")
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_dateInicio_dateInput').send_keys(i)
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_dateFin_dateInput').send_keys(i)
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_chkTabla').click()
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_btnver').click()
    time.sleep(1)
    driver.get("http://10.50.128.91/GestSAE/Informes/VisorInformes.aspx")
    time.sleep(5)
    driver.find_element('id','ReportViewer1_ctl01_ctl05_ctl00').send_keys('CSV (delimitado por comas)')
    time.sleep(2)
    driver.find_element('id','ReportViewer1_ctl01_ctl05_ctl01').click()
    time.sleep(1)
    driver.refresh()

    # descarga estado de conductores

    driver.get("http://10.50.128.91/GestSAE/Informes/CondEstadoConductores.aspx")
    time.sleep(1)
    driver.find_element('id','ctl00_MainContent_btnver').click()
    time.sleep(1)
    driver.get("http://10.50.128.91/GestSAE/Informes/VisorInformes.aspx")
    time.sleep(5)
    driver.find_element('id','ReportViewer1_ctl01_ctl05_ctl00').send_keys('CSV (delimitado por comas)')
    time.sleep(2)
    driver.find_element('id','ReportViewer1_ctl01_ctl05_ctl01').click()
    time.sleep(1)
    driver.refresh()

    # creacion de directorios -----------------------------------------------------------------------------------------
    files_to_copy = [
        {
            'download_path': 'C:\\Users\\javier.tellez\\Downloads\\InoperablesPorEmpresa.csv',
            'local_folder': 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\12 inoperables',
            'prefix': dia_ajus,
            'suffix': '_inoperables_UF17.csv'
        },
        {
            'download_path': 'C:\\Users\\javier.tellez\\Downloads\\AccDetalleEventosTransitoIntegrado.csv',
            'local_folder': 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\14 accidente transito',
            'prefix': dia_ajus,
            'suffix': '_accidente_transito_UF17.csv'
        },
        {
            'download_path': 'C:\\Users\\javier.tellez\\Downloads\\AccDetalleEventosEstacionIntegrado.csv',
            'local_folder': 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\16 accidente estacion',
            'prefix': dia_ajus,
            'suffix': '_accidente_estacion_UF17.csv'
        },
        {
            'download_path': 'C:\\Users\\javier.tellez\\Downloads\\AccDetalleEventosConvivenciaIntegrado.csv',
            'local_folder': 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\18 convivencia',
            'prefix': dia_ajus,
            'suffix': '_convivencia_UF17.csv'
        },
        {
            'download_path': 'C:\\Users\\javier.tellez\\Downloads\\EstadoConductores.csv',
            'local_folder': 'G:\\Unidades compartidas\\GM_OP_ANALISIS_DE_DATOS\\20 estado conductor',
            'prefix': dia_ajus,
            'suffix': '_estado_conductor_UF17.csv'
        }
    ]
    # ciclo para copiar los archivos en un nuevo directorio
    for file in files_to_copy:
        download_path = file['download_path']
        local_folder = file['local_folder']
        prefix = file['prefix']
        suffix = file['suffix']
        filename = prefix + suffix
        new_file_path = os.path.join(local_folder, filename)
        
        os.makedirs(local_folder, exist_ok=True)
        shutil.copy(download_path, new_file_path)
        os.remove(download_path)

driver.close()
print("proceso terminado")

