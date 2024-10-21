import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup 
import re
import time
from mysql.connector.errors import ProgrammingError 
from db import nova_conexao
from mysql.connector import connect
from datetime import datetime as dt
import customtkinter as tk


def scraapy(content , D, T):

    #regex
    name = re.compile("(\">)(.*)(</a>)")
    powerRe = re.compile("[0-9]{1,3}[.][0-9]{1,3}")

    #aqui estou sendo mais especifico, tentando pegar elementos mais filtrado para nome e potencia
    page = BeautifulSoup(content, "html.parser")
    nomeHTML = page.find_all("a" , class_="nco-home-list-table-name nco-home-list-text-ellipsis")
    potHTML = page.find_all("div" , class_="nco-cloumn-eqPowerHours")
    # mostra o tamanho de cada coleta
    # print(len(nomeHTML))
    # print(len(potHTML))
    for i in range(0, len(nomeHTML) ):

        # print(re.findall(name , str(nomeHTML[i])))
        res = name.finditer(str(nomeHTML[i]))
        for x in res:
            inv = [x.group(2)]

        pot = re.findall(powerRe , str(potHTML[i*4]))
        # print(pot)
        # print(inv)        
        database(str(inv) , str(pot) , D , T)


#cria a conexão com o banco de dados e envia dados para DB       
def database(x, y , D , T):
    inv = x[1:-1]
    pot = y[1:-1]
   
    
    # data_formatada = time.strftime('%Y-%m-%d %H:%M:%S')
    sql1 = "INSERT INTO `{}` (Date, TimeStamp , POTÊNCIA) VALUES ('{}' , '{}' , '{}')".format(inv.replace("\'", "") , D, T ,  pot.replace("\'", ""))
    
    with nova_conexao() as conexao:
        try:
            cursor = conexao.cursor()       
            cursor.execute(sql1)
            conexao.commit() 
            cursor.close()
              
        except ProgrammingError as e:
            print(f"Erro: {e.msg}")
        else:
            print(f"Foram incluidos {cursor.rowcount} registros!")


while True:
    #variável que coleta a hora
    hora = dt.now()
    #mostra a data a hora e os minutos, 21/02/2024 , 09:33
    TimeStamp = hora.strftime("%H:%M")
    Data = hora.strftime("%d/%m/%Y")

    if(hora.hour >= 8 and hora.hour <= 18):
    
        with sync_playwright() as p:
            # teraenergia / energiafv01  
            #bot abre o site e navegar ate ter as informaçoes do inversor
            navegator = p.chromium.launch(headless=False) #headless mostra ou n o navegador
            page = navegator.new_page()
            page.goto("https://la5.fusionsolar.huawei.com/uniportal/pvmswebsite/assets/build/cloud.html")

            time.sleep(0.1)

            #localiza o campo de preenchimento e preenche
            page.fill("xpath=/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/input" , mail)
            page.fill("xpath=/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/input" , password)
            time.sleep(0.1)

            #localiza o elemento na pagina e clica login
            page.locator('xpath=/html/body/div[1]/div[2]/div[2]/div[3]/div/span').click()
            time.sleep(10)

            #faz com que todos os inversores fiquem disponíveis
            page.locator('xpath=/html/body/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div[4]/ul/li[11]/div[1]/div/span[2]').click()
            time.sleep(0.1)
            #abre o pop-up e seleciona o elemento 100, para mostrar todos os inversores
            page.locator('xpath=/html/body/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/div/div/div[2]/div[4]/ul/li[11]/div[1]/div[2]/div/div/div/div[2]/div/div/div/div[5]/div').click()
            time.sleep(2)

            
            scraapy(page.content() , Data , TimeStamp)
            page.close()
            time.sleep(3000)


