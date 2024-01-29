import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup 
import re
import time


#bot abre o site e navegar ate ter as informaçoes do inversor
with sync_playwright() as p:

    navegator = p.chromium.launch(headless=False) #headless mostra ou n o navegador
    page = navegator.new_page()
    page.goto("https://la5.fusionsolar.huawei.com/uniportal/pvmswebsite/assets/build/cloud.html")

    time.sleep(3)

     #localiza o campo de preenchimento e preenche
    page.fill("xpath=/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/input" , "teraenergia")
    page.fill("xpath=/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/input" , "energiafv01")
    time.sleep(2)

    #localiza o elemento na pagina e clica
    page.locator('xpath=/html/body/div[1]/div[2]/div[2]/div[3]/div/span').click()
    time.sleep(5)
    page.locator('xpath=/html/body/div/div/div/div[1]/div/div[1]/div[2]/ul/li[2]/div/div/div/div/div/a/span[2]').click()
    time.sleep(5)

   