#Importación de librerías y módulos

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from chromedriver_py import binary_path
from openpyxl import load_workbook
from datetime import datetime
import os
from dotenv import load_dotenv
import requests
from lxml import html

## La función main llama a las funciones encargadas del webscrapping y desempaca los valores que cada una devuelve. 
## Luego abre un documento excel y añade los valores scrappeados.
## Finalmente cierra el documento e imprime un mensaje a pantalla para confirmar que el programa corrió correctamente. 

def main():
    load_dotenv()
    user = os.environ.get('Byma')
    password = os.environ.get('PASSWORD')

    dia = datetime.now().strftime('%Y-%m-%d')
    valor_al30, valor_al30C, valor_al30D = obtener_valores_mep(user, password)
    bna, blue, mayorista = dolares()
    
    #Abre el excel al que cargo los datos.
    doc = load_workbook('Calculadoras.xlsx')
    hoja= doc['Calc MEP-CCL']

    hoja['C5'].value = hoja['C6'].value
    hoja['F5'].value = hoja['F6'].value
    hoja['C3'].value = valor_al30
    hoja['F3'].value = valor_al30
    hoja['C4'].value = valor_al30C
    hoja['F4'].value = valor_al30D
    hoja['I4'].value = blue
    hoja['I9'].value = bna
    hoja['I14'].value = mayorista

    doc.save('Calculadoras_update.xlsx')

    print(f'Valores actualizados: bna = {bna}, mayorista = {mayorista}')

def valor_numerico(elemento): #transforma elemento html en un valor numérico flotante: de '$1000' a 1000.0
    string = elemento[0].text
    number = string.replace('$', '').strip()
    return float(number)

#Obtiene los valores de Dolar Banco Nación, Dolar Blue y Dolar Mayorista.
def dolares():
    response = requests.get('https://www.cotizacion-dolar.com.ar/dolar-hoy?gclid=Cj0KCQjwlK-WBhDjARIsAO2sErRwtZoNktatL2qNNQ2DqqZezDDNqOzUMaKUCbeXP9MiUROl8J7DXuYaAox7EALw_wcB ')
    tree = html.fromstring(response.content)

    valores_dolar = {
    'dolar_bna': '/html/body/div[2]/section/div/div[1]/article/div[1]/div[2]/div[2]/div[2]/span',
    'blue': '/html/body/div[2]/section/div/div[1]/article/div[1]/div[2]/div[4]/div[2]/span',
    'mayorista': '/html/body/div[2]/section/div/div[1]/article/div[1]/div[2]/div[5]/div[2]/span',
}
    for dolar in valores_dolar:
        valores_dolar[dolar]= valor_numerico(tree.xpath(valores_dolar[dolar]))

    return(valores_dolar.values())

#Obtiene el valor del bono AL30 para calcular el Dolar MEP.
def obtener_valores_mep(username, password):
    # Accede al username y password desde variables de entorno

    svc = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(service=svc)
        
    driver.get('https://new2.bymadata.com.ar/#/auth/login')
    username_field = driver.find_element('name', "username")
    username_field.send_keys(username)

    password_field = driver.find_element('name', "password")
    password_field.send_keys(password)

    password_field.send_keys(Keys.ENTER)
    
    time.sleep(10)  #da tiempo a loggearse

    # Ahora accedemos a la página que deseamos dentro de byma.
    driver.get("https://new2.bymadata.com.ar/#/market-depth")
    driver.implicitly_wait(30) #espera para que no de error.

    #Xpaths de los valores a scrappear
    al30d_xpath = '/html/body/app-root/app-main-layout/div/sa-market-depth/mdp-pane/div/ngx-gridster/div/ngx-gridster-item[34]/div/div[1]/div/mdp-widget/div/mdp-price-depth-content/div/div[1]/table/tbody/tr[1]/td[4]'
    al30_xpath = '/html/body/app-root/app-main-layout/div/sa-market-depth/mdp-pane/div/ngx-gridster/div/ngx-gridster-item[35]/div/div[1]/div/mdp-widget/div/mdp-price-depth-content/div/div[1]/table/tbody/tr[1]/td[4]'
    al30c_xpath =  '/html/body/app-root/app-main-layout/div/sa-market-depth/mdp-pane/div/ngx-gridster/div/ngx-gridster-item[33]/div/div[1]/div/mdp-widget/div/mdp-price-depth-content/div/div[1]/table/tbody/tr[1]/td[4]'
    
    #Consigo los valores deseados, accedo al texto y los transformo a valor flotante. 
    al30d=driver.find_element(By.XPATH, al30d_xpath)
    valor_al30D= float(al30d.get_attribute("textContent").replace('.' ,'').replace(',' ,'.'))

    al30=driver.find_element(By.XPATH, al30_xpath)
    valor_al30= float(al30.get_attribute("textContent").replace('.' ,'').replace(',', '.'))

    al30c=driver.find_element(By.XPATH, al30c_xpath)
    valor_al30C= float(al30c.get_attribute("textContent").replace('.' ,'').replace(',' ,'.'))

    driver.quit()
    print('Valores scrappeados')

    return ([valor_al30, valor_al30C , valor_al30D])

if __name__ == "__main__":
    main()
