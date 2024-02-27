import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup 
import re
import time
from mysql.connector.errors import ProgrammingError 
from db import nova_conexao
from mysql.connector import connect



def scraapy(content):

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
        
        print(inv)
        

        # print(jj[1:-1])
        create(str(inv))
        time.sleep(0.2)



def create(x):

    y = x[1:-1]
    # print(y.replace("\'" , " "))
    
    tabela_inversores = '''
        CREATE TABLE `{}`(
            Date VARCHAR(50),
            TimeStamp varchar(50), 
            POTÊNCIA VARCHAR(40),
            id INT AUTO_INCREMENT PRIMARY KEY
            
            )
    '''.format(y.replace("\'",""))
  

    with nova_conexao() as conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute(tabela_inversores)

        except ProgrammingError as e:
            print(f"Erro: {e.msg}")


#bot abre o site e navegar ate ter as informaçoes do inversor
with sync_playwright() as p:

    navegator = p.chromium.launch(headless=False) #headless mostra ou n o navegador
    page = navegator.new_page()
    page.goto("https://la5.fusionsolar.huawei.com/uniportal/pvmswebsite/assets/build/cloud.html")

    time.sleep(0.1)

    #localiza o campo de preenchimento e preenche
    page.fill("xpath=/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/input" , "teraenergia")
    page.fill("xpath=/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/input" , "energiafv01")
    time.sleep(0.1)

    #localiza o elemento na pagina e clica login
    page.locator('xpath=/html/body/div[1]/div[2]/div[2]/div[3]/div/span').click()
    time.sleep(2)

    #faz com que todos os inversores fiquem disponíveis
    page.locator('xpath=/html/body/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div[4]/ul/li[11]/div[1]/div/span[2]').click()
    time.sleep(0.1)
    #abre o pop-up e seleciona o elemento 100, para mostrar todos os inversores
    page.locator('xpath=/html/body/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/div/div/div[2]/div[4]/ul/li[11]/div[1]/div[2]/div/div/div/div[2]/div/div/div/div[5]/div').click()
    time.sleep(2)

    
    scraapy(page.content())
       