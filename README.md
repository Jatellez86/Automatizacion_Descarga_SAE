
# 📊 GetstSAE Data Scraper - UF17 🚀

## 📘 Descripción

Este script de Python 🐍 está diseñado para automatizar la descarga de varios informes del sistema GetsSAE para una unidad funcional del SITP. Utiliza la biblioteca Selenium 🌐 para navegar y manipular la interfaz web del sistema, en general conecta con la pagina web, descarga datos, los organiza y lleva a un Datalake para luego ser transformados y cargados a un base de datos.

---
<span style="color:blue">_______________________________________________________________________________________</span>

## 📦 Dependencias

- **Selenium 🌐**
  - `webdriver`
  - `Keys`
  - `By`
- **Pandas 🐼**
- **Datetime ⏰**
- **Time**
- **OS**
- **Shutil**

---
<span style="color:green">_______________________________________________________________________________________</span>

## 📋 Funcionamiento General

1. **🌟 Inicialización**: Importa todas las bibliotecas requeridas y configura las variables iniciales, incluyendo credenciales y fechas para la descarga de informes.
2. **📆 Preparación de Fechas**: Utiliza el módulo `Datetime` para generar un DataFrame de fechas objetivo para la descarga de informes.
3. **🤖 Automatización del Navegador**: Implementa Selenium para abrir y manipular un navegador web. La función `openBrowser` inicializa este proceso.
4. **📥 Descarga de Informes**: Utiliza bucles para iterar a través de las fechas y archivos, descargando los informes correspondientes.
5. **🗂️ Almacenamiento de Datos**: Emplea los módulos `OS` y `Shutil` y uso de diccionarios para organizar y almacenar los informes descargados en directorios específicos.

---
<span style="color:blue">_______________________________________________________________________________________</span>

## 🚀 Uso

1. Asegúrese de tener todas las bibliotecas requeridas instaladas 📚.
2. Configure las variables relevantes como credenciales de inicio de sesión y rutas de almacenamiento 🛠️.
3. Ejecute el script 🖥️.

---
<span style="color:green">_______________________________________________________________________________________</span>

## 👥 Autores

- **Javier Tellez 🙋‍♂️**

---
<span style="color:blue">_______________________________________________________________________________________</span>

## 📅 Fecha

- **21 de marzo de 2023**

---
<span style="color:green">_______________________________________________________________________________________</span>

- **21 de marzo de 2023**


