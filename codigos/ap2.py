from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

navegador = webdriver.Chrome()

navegador.get('https://www.aliexpress.us/')

nome = '//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[1]/div/div/a/div[2]/div[1]'
navegador.find_element(By.XPATH, nome).text

preco_com_desconto = '//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[1]/div/div/a/div[2]/div[2]/div[1]'
navegador.find_element(By.XPATH, preco_com_desconto).text

preco_sem_desconto1 = '//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[1]/div/div/a/div[2]/div[2]/div[2]/span'
navegador.find_element(By.XPATH, preco_sem_desconto1).text

###################################################

nome2 = '//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[2]/div/div/a/div[2]/div[1]/h3'
navegador.find_element(By.XPATH, nome2).text

preco2 = '//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[2]/div/div/a/div[2]/div[2]/div[1]'
navegador.find_element(By.XPATH, preco2).text

precoSemDesconto2 = '//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[2]/div/div/a/div[2]/div[2]/div[2]/span'

##################################################

nome3 = '//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[3]/div/div/a/div[2]/div[1]'
navegador.find_element(By.XPATH, nome3).text

preco3 = '//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[3]/div/div/a/div[2]/div[3]/div[1]'
navegador.find_element(By.XPATH, preco3).text

precoSemDesconto3 = '//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[3]/div/div/a/div[2]/div[3]/div[2]/span'

'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[1]/div/div/a/div[2]/div[1]'
'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[2]/div/div/a/div[2]/div[1]'
'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[3]/div/div/a/div[2]/div[1]'


'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[1]/div/div/a/div[2]/div[2]/div[1]'
'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[2]/div/div/a/div[2]/div[3]/div[1]'
'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[3]/div/div/a/div[2]/div[3]/div[1]'

'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[1]/div/div/a/div[2]/div[3]/div[2]/span'
'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[2]/div/div/a/div[2]/div[3]/div[2]/span'
'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[3]/div/div/a/div[2]/div[3]/div[2]/span'




lista_produtos = [] # lista vazia
for produto in range(1,31):
    try:
       # print(navegador.find_element(By.XPATH, f'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[{produto}]/div/div/a/div[2]/div[1]').text)
        dado_produto = navegador.find_element(By.XPATH, f'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[{produto}]/div/div/a/div[2]/div[1]').text
        lista_produtos.append(dado_produto)
    except:
        pass

lista_preco_com_desconto = [] # lista vazia
for preco_com_desconto in range(1,31):
    try:
        #print(navegador.find_element(By.XPATH, f'//*[@id=":Ra{preco}j7:"]/div[2]/div[1]/div').text)
        dado_preco_com_desconto = navegador.find_element(By.XPATH, f'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[{preco_com_desconto}]/div/div/a/div[2]/div[2]/div[1]').text
        lista_preco_com_desconto.append(dado_preco_com_desconto)
    except:
        pass

lista_preco_sem_desconto = [] # lista vazia
for preco_sem_desconto in range(1,31):
    try:
        #print(navegador.find_element(By.XPATH, f'//*[@id=":Ra{preco}j7:"]/div[2]/div[1]/div').text)
        dado_preco_sem_desconto = navegador.find_element(By.XPATH, f'//*[@id="root"]/div[2]/div[7]/div/div/div/div[2]/div[{preco_sem_desconto}]/div/div/a/div[2]/div[2]/div[2]/span').text
        lista_preco_sem_desconto.append(dado_preco_sem_desconto)
    except:
        pass

##EXIBINDO AS VARIAVEIS
lista_preco_sem_desconto

lista_preco_com_desconto

lista_produtos

#########
import pandas as pd
tabela1 = pd.DataFrame(lista_produtos, columns=['produto'])
tabela1

tabela2 = pd.DataFrame(lista_preco_com_desconto, columns=['preco_com_desconto'])
tabela2

tabela3 = pd.DataFrame(lista_preco_sem_desconto, columns=['preco_sem_desconto'])
tabela3

df = pd.concat([tabela1, tabela2, tabela3], axis=1)

df

import csv 
df.to_csv('../projeto_AP2/bases_originais/produtos.csv', sep=';', index=False, encoding='utf-8')

#df.to_excel('produtos.xlsx')

###################################################################################################

#Tratamento de dados

#pip install unidecode

import pandas as pd
import numpy as np
#import missingno as msno
import plotly.express as px
#import unidecode

dados = pd.read_csv('../projeto_AP2/bases_originais/produtos.csv', sep=';', encoding='utf-8')

dados

# verificando o tamanho da base em linhas e colunas
dados.shape
dados.columns

#resentando o index e removendo duplicados
dados = dados.reset_index(drop=True)

#Tratando a coluna com NaN, como não teve alteração de desconto mantivemos o preço
dados['preco_sem_desconto'] = dados['preco_sem_desconto'].fillna(dados['preco_com_desconto'])

dados['preco_com_desconto'] = dados['preco_com_desconto'].fillna(dados['preco_sem_desconto'])

#tratamento nulo
dados.preco_sem_desconto.fillna(0, inplace=True)
dados.preco_com_desconto.fillna(0, inplace=True)

dados.produto.fillna('missing', inplace=True)

#Tratando os dados da coluna preço, removendo R$, e vírgula por ponto

dados['preco_com_desconto'] = (
    dados['preco_com_desconto']
    .str.replace('R$', '', regex=False)     # remove o 'R$'
    .str.replace('.', '', regex=False)      # remove separadores de milhar
    .str.replace(',', '.', regex=False)     # troca vírgula por ponto decimal
    .astype(float)                          # converte para float
)


#Tratando os dados da coluna preço, removendo R$, e vírgula por ponto
dados['preco_sem_desconto'] = (
    dados['preco_sem_desconto']
    .str.replace('R$', '', regex=False)     # remove o 'R$'
    .str.replace('.', '', regex=False)      # remove separadores de milhar
    .str.replace(',', '.', regex=False)     # troca vírgula por ponto decimal
    .astype(float)                          # converte para float
)

#Validando se os dados foram tratados
dados

# #tratamento duplicatas

baseTratada = dados.drop_duplicates()

#outliers

baseTratada.loc[baseTratada.preco_sem_desconto > 999, 'preco_sem_desconto']=999

baseTratada.loc[baseTratada.preco_com_desconto > 999, 'preco_com_desconto']=999


baseTratada.loc[baseTratada.preco_sem_desconto < 0, 'preco_sem_desconto']=100

baseTratada.loc[baseTratada.preco_com_desconto < 0, 'preco_com_desconto']=100


#exportando a base tratada
import csv
baseTratada.to_csv('../projeto_AP2/bases_tratadas/dados_tratados.csv', sep=';', index=False, encoding='utf-8')


#criar um arquivo bibliotecas.txt em codigos com as seguintes libs
# streamlit
# plotly
# unicode
# missingno


