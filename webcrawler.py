# -*- coding: utf-8 -*-

nome_usuario = "Coimbra_develop"
senha_usuario = "GuilhermeX@24"

import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def extrair_tweet_e_sentimento(tweet):
  texto_tweet = tweet.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']").text
  sentimento = analyzer.polarity_scores(texto_tweet)
  return {"texto": texto_tweet, "sentimento": sentimento}

service = Service()
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(service=service, options=options)
analyzer = SentimentIntensityAnalyzer()


driver.get("https://twitter.com/")
time.sleep(2)
login = driver.find_element(By.CSS_SELECTOR, "a.css-175oi2r:nth-child(2) > div:nth-child(1)")
login.click()
time.sleep(3)
usuario = driver.find_element(By.CSS_SELECTOR, "div.css-175oi2r input")
usuario.send_keys(nome_usuario)
usuario.send_keys(Keys.ENTER)
time.sleep(3)
senha = driver.find_element(By.XPATH, "//input[@autocomplete='current-password']")
senha.send_keys(senha_usuario)
senha.send_keys(Keys.ENTER)
time.sleep(3)
campo_pesquisa = driver.find_element(By.CSS_SELECTOR, "div.css-146c3p1 input")
# NOTE mexer aqui para colocar o que contem a palavra
campo_pesquisa.send_keys("estressante")
campo_pesquisa.send_keys(Keys.ENTER)
time.sleep(5)

lista_tweets = []
tweets = driver.find_elements(By.TAG_NAME, "article")
for tweet in tweets:
  dados_tweet = extrair_tweet_e_sentimento(tweet)
  print(dados_tweet)
  lista_tweets.append(dados_tweet)

df_tweets = pd.DataFrame(lista_tweets)
df_tweets.to_csv("tweets_estresse.csv", index=False)


driver.quit()

def levenshtein(nome1, nome2):
    if len(nome1) < len(nome2):
        return levenshtein(nome2, nome1)
    if len(nome2) == 0:
        return len(nome1)

    linha_anterior = range(len(nome2) + 1)
    for i, c1 in enumerate(nome1):
        linha_atual = [i + 1]
        for j, c2 in enumerate(nome2):
            insercao = linha_anterior[j + 1] + 1
            exclusao = linha_atual[j] + 1
            substituicao = linha_anterior[j] + (c1 != c2)
            linha_atual.append(min(insercao, exclusao, substituicao))
        linha_anterior = linha_atual

    return linha_anterior[-1]

def correcao_nome(nome_incorreto, nome_correto, limiar):
    distancia = levenshtein(nome_incorreto, nome_correto)
    return distancia <= limiar

def destacar_diferencas(nome_incorreto, nome_correto):
    resultado = []
    tamanho_max = max(len(nome_incorreto), len(nome_correto))

    for i in range(tamanho_max):
        if i < len(nome_incorreto) and i < len(nome_correto):
            if nome_incorreto[i] != nome_correto[i]:
                resultado.append(f"\033[91m{nome_incorreto[i]}\033[0m")  # Vermelho para letras diferentes
            else:
                resultado.append(nome_incorreto[i])
        elif i < len(nome_incorreto):
            resultado.append(f"\033[91m{nome_incorreto[i]}\033[0m")  # Vermelho para letras adicionais no nome incorreto
        else:
            resultado.append(f"\033[92m{nome_correto[i]}\033[0m")  # Verde para letras faltantes no nome incorreto

    return ''.join(resultado)

nome_correto = "puta"
nomes_incorretos = ["put@", "puto", "p!t@", "cachorro", "poca"]
limiar = 4

for nome_incorreto in nomes_incorretos:
    if correcao_nome(nome_incorreto, nome_correto, limiar):
        print(f"Você quis dizer '{nome_correto}' em vez de '"+ destacar_diferencas(nome_incorreto, nome_correto) +"'?")