from db import nova_conexao
import time
from datetime import datetime as dt
import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup 
import re
import smtplib
import email.message


lista_mau = []
lista_funcionando = []

hora = dt.now()
Data = hora.strftime("%d/%m/%Y")

def email_automatico():
    corpo_email = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Título Centralizado</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            .titulo {{
                text-align: center;
                color: white;
                background-color: red;
                padding: 10px;
            }}
        </style>
    </head>
    <body>

    <div class='titulo'>
        <h1>Lista de Inversores com Mau Funcionamento</h1>
        <h2>{}</h2>
    </div>

    <div>
        <p>{}</p>
    </div>

    </body>
    </html>

    """.format(Data , '<br>'.join(lista_mau))

    msg = email.message.Message()
    msg['Subject'] = "Lista de Inversores"
    msg['From'] = 'viniciusalfredo.s@gmail.com'
    msg['To'] = 'pimentasinatra69@gmail.com'
    password = 'suym olqj ayix fhtn' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')  

def analise(nome):
    with nova_conexao() as conexao:
      
        y = nome[1:-1]
        cursor = conexao.cursor()       
        cursor.execute("SELECT POTÊNCIA FROM `{}` WHERE Date = '{}'".format(y.replace("\'","") , Data))
        x = cursor.fetchall()
        soma = 0
        for i in range(len(x)):
            soma += float(x[i][0])   

        if(soma <= 1):
            lista_mau.append("{}".format(y.replace("\'","")))
        else:
            lista_funcionando.append("{}".format(y))

def scraapy(content):

    #regex
    name = re.compile("(\">)(.*)(</a>)")
    page = BeautifulSoup(content, "html.parser")
    nomeHTML = page.find_all("a" , class_="nco-home-list-table-name nco-home-list-text-ellipsis")  

    for i in range(0, len(nomeHTML) ):

        # print(re.findall(name , str(nomeHTML[i])))
        res = name.finditer(str(nomeHTML[i]))
        for x in res:
            inv = [x.group(2)]
      
        # print(inv)
        analise(str(inv))
     
#if(hora.hour() == 19)
with sync_playwright() as p:

    navegator = p.chromium.launch(headless=False) #headless mostra ou n o navegador
    page = navegator.new_page()
    page.goto("https://la5.fusionsolar.huawei.com/uniportal/pvmswebsite/assets/build/cloud.html")

    time.sleep(0.1)

    #localiza o campo de preenchimento e preenche
    page.fill("xpath=/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/input" , "teraenergia")
    page.fill("xpath=/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/input" , "energiafv01")
    time.sleep(0.1)
    page.locator('xpath=/html/body/div[1]/div[2]/div[2]/div[3]/div/span').click()
    time.sleep(2)
    page.locator('xpath=/html/body/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div[4]/ul/li[11]/div[1]/div/span[2]').click()
    time.sleep(0.1)
    page.locator('xpath=/html/body/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/div/div/div[2]/div[4]/ul/li[11]/div[1]/div[2]/div/div/div/div[2]/div/div/div/div[5]/div').click()
    time.sleep(2)

    scraapy(page.content())
    print(lista_mau)
    email_automatico()
    #time.sleep(3601)
    

    
            
  