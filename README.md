# Web Scraping de valores del Dolar Estadounidense en Argentina
Este proyecto es una herramienta de web scraping diseñada para obtener datos financieros de varias fuentes en línea. Utiliza Selenium para automatizar la navegación web y OpenPyXL para actualizar un archivo Excel con los últimos datos recopilados.

En Argentina existen muchos valores del dolar estadounidense. Se puede comprar dólares de manera legal, en el mercado paralelo (lo que se conoce como **dolar blue**) o incluso a través de los bonos AL30 (**dolar mep**). 
Obviamente, en Argentina estos valores cambian todos los días. 

Este programa scrappea esos valores, algunos disponibles abiertamente y otros desde la página oficial de la bolsas y Mercados Argentinos (**BYMA**). Y los inserta en un excel para su posterior análisis. 

## Características
Inicia sesión en el sitio web de BYMA con credenciales de usuario.
Allí obtiene el valor de los bonos. 
Además accede a los valores del "Dolar Banco Nación", "Dolar Blue" y "Dolar Mayorista" desde una página libre. 
Actualiza un archivo Excel con los datos recopilados.
Funciona con programación asíncrona para una ejecución eficiente.

## Requisitos
Python 3.6 o superior \
Chrome WebDriver\
Bibliotecas de Python: selenium, openpyxl, python-dotenv, chromedriver-py

## Instalación
Clona este repositorio en tu máquina local:\
git clone https://github.com/RadTorino/Scrapping-Valores-Dolar.git\
Instala las dependencias utilizando pip:

*pip install -r requirements.txt*

Descarga el Chrome WebDriver (https://chromedriver.chromium.org/downloads/version-selection) e incluye la ruta en tu sistema.

## Uso
Asegúrate de tener el archivo .env configurado con las credenciales necesarias.\
Ejecuta el archivo main.py para iniciar el proceso de web scraping:

*python main.py*

Los datos actualizados se guardarán en un archivo Excel con el nombre Calculadoras_update.xlsx.

## Contribución
Las contribuciones son bienvenidas. Si encuentras un problema o tienes una idea para mejorar el proyecto, abre un issue o envía una pull request.

## Licencia
Este proyecto está bajo la licencia MIT.

